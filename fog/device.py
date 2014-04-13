__author__ = 'Raghav Sidhanti'

import mimetypes
import message
import fsutil

from inout import StdIn
from inout import StdOut
from configuration import Conf
from configuration import ConfUtil

from apiclient.discovery import build
from apiclient.http import  MediaFileUpload
from httplib2 import Http
from oauth2client.file import Storage
from oauth2client.tools import run
from oauth2client.client import OAuth2WebServerFlow

# define the list of devices and their behaviours


def get_active_drive():
    # get configs
    checkout = ConfUtil.get_checkout()
    # retrieve active drive
    if checkout:
        return get_drive(checkout)
    return None


def get_drive(name):
    return {
        GoogleDrive.name(): lambda: GoogleDrive()
    }.get(name, lambda: None)()


class Drive(object):
    @staticmethod
    def name():
        pass

    def open(self, **kwargs):
        pass

    def close(self, **kwargs):
        pass

    def download(self, **kwargs):
        pass

    def upload(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class GoogleDrive(Drive):
    __drive = None
    __http = None

    __FOLDER_MIME = 'application/vnd.google-apps.folder'

    @staticmethod
    def __get_credentials():

        storage = Storage(ConfUtil.get_drive_prop(Conf.GOOGLE, Conf.CREDENTIALS))
        credentials = storage.get()

        # if no credentials
        if credentials is None or credentials.invalid:
            # validate credentials
            client_id = StdIn.prompt(message.get(message.GOOGLE_ID))
            client_secret = StdIn.prompt(message.get(message.GOOGLE_SECRET))

            if not client_id or not client_secret:
                StdOut.display(msg=message.get(message.INVALID_CREDENTIALS))
                return None

            StdOut.display(msg=message.GOOGLE_CONSENT)
            # run flow and store credentials
            flow = OAuth2WebServerFlow(client_id, client_secret, 'https://www.googleapis.com/auth/drive')
            credentials = run(flow, storage)

        return credentials

    def __find_meta(self, path=''):
        # preconditions
        if not path:
            return None

        # split file and cleanup
        titles = fsutil.split(path)
        # pick the last element and search for it in google drive
        req = self.__drive.files().list()
        while req:
            resp = req.execute()
            metas = resp.get('items')
            for meta in metas:
                index = len(titles) - 1
                # if found,
                if meta.get('title') == titles[index]:
                    # retrieve its ancestors and compare against titles
                    parent = meta.get('parents')[0]
                    while True:
                        # if is root and reached end, return
                        if parent.get('isRoot') and index == 0:
                            return meta

                        # if not reached end and equal titles, continue
                        if not parent.get('isRoot') and index > 0:
                            index -= 1
                            anc = self.__drive.files().get(fileId=parent.get('id')).execute()
                            if anc.get('title') == titles[index]:
                                parent = anc.get('parents')[0]
                                continue
                        break
            # paginate
            req = self.__drive.files().list_next(req, resp)
        return None

    def __write(self, meta, dst):
        if meta is None or not dst:
            return

        # if folder, persist all its children
        if meta.get('mimeType') == self.__FOLDER_MIME:
            self.__write_folder(meta, dst)
        else:
            # if file, persist
            self.__write_file(meta, dst)

    def __write_file(self, meta, dst):
        url = meta.get('downloadUrl', None)
        # todo google document types not supported at this time
        content = self.__get_content(url)
        if content is None:
            StdOut.display(msg=message.get(message.ERROR_DOWNLOAD, file=meta.get('title'), drive=self.name()))
        fsutil.write(dst, content, True)

    def __write_folder(self, meta, dst):
        # create folder if it does not exist
        fsutil.create_dir(dst)
        # list all its children,
        children = self.__drive.children().list(folderId=meta.get('id')).execute()
        for child in children.get('items'):
            child_meta = self.__drive.files().get(fileId=child.get('id')).execute()
            child_dst = fsutil.join_paths(dst, child_meta.get('title'))
            # if child is folder, recurs
            if child_meta.get('mimeType') == self.__FOLDER_MIME:
                self.__write_folder(child_meta, child_dst)
            # if child is file, write it to folder
            else:
                self.__write_file(child_meta, child_dst)

    def __get_content(self, url):
        if not url:
            return None

        resp, content = self.__http.request(url)
        if resp.get('status') != '200':
            return None
        return content

    def __insert(self, path, meta):
        if not path or not meta:
            return

        if fsutil.is_folder(path):
            self.__insert_folder(path, meta)
        else:
            self.__insert_file(path, meta)

    def __insert_file(self, src=None, meta=None):
        file_name = fsutil.filename(src)
        media = MediaFileUpload(src, resumable=True)
        children = self.__drive.children().list(folderId=meta.get('id')).execute()
        for child in children:
            child_meta = self.__drive.files().get(fileId=child.get('id')).execute()
            if child_meta.get('title') == file_name:
                if StdIn.prompt_yes(msg=message.get(message.PROMPT_OVERWRITE, file=file_name)):
                    self.__drive.files().update(fileId=child_meta.get(id), media_body=media).execute()
                    return
        body = {
            'title': file_name
        }
        self.__drive.children().insert(folderId=meta.get('id'), media_body=media, body=body)

    def __insert_folder(self, src=None, meta=None):
        folder_name = fsutil.filename(src)
        children = self.__drive.children().list(folderId=meta.get('id')).execute()
        folder_meta = None
        for child in children:
            child_meta = self.__drive.files().get(fileId=child.get('id')).execute()
            if child_meta.get('title') == folder_name and child_meta.get('mimeType') == self.__FOLDER_MIME:
                folder_meta = child_meta
                break

        if folder_meta is None:
            body = {
                'title': folder_name,
                'mimeType': self.__FOLDER_MIME
            }
            folder_meta = self.__drive.children().insert(folderId=meta.get('id'), body=body).execute()

        for path in fsutil.list_folder(src):
            self.__insert(path, folder_meta)

    @staticmethod
    def name():
        return Conf.GOOGLE

    def open(self, **kwargs):

        credentials = self.__get_credentials()

        if credentials is not None:
            # if every thing is good, authorize http and build drive
            self.__http = credentials.authorize(Http())
            self.__drive = build('drive', 'v2', http=self.__http)
            return True

        return False

    def close(self, **kwargs):
        self.__drive = None
        self.__http = None

    def download(self, **kwargs):
        src = kwargs.get('src', None)
        dst = kwargs.get('dst', None)

        # find and persist
        meta = self.__find_meta(src)
        if meta is not None:
            self.__write(meta, dst)
        else:
            # file not found
            StdOut.display(msg=message.get(message.MISSING_FILE, location=self.name()))

    def delete(self, **kwargs):
        src = kwargs.get('src', None)

        # find file
        meta = self.__find_meta(src)
        if meta is not None:
            if StdIn.prompt_yes(message.get(message.PROMPT_TRASH, file=src, drive=self.name())):
                # delete the file
                resp = self.__drive.files().trash(fileId=meta.get('id')).execute()
                if resp:
                    StdOut.display(message.get(message.TRASH, file=src, drive=self.name()))
        else:
            StdOut.display(msg=message.get(message.MISSING_FILE, location=self.name()))

    def upload(self, **kwargs):
        src = kwargs.get('src', None)
        dst = kwargs.get('dst', None)

        # if not folder, print error and return
        if not fsutil.exists(src):
            StdOut.display(msg=message.get(message.MISSING_FILE, location='local'))
            return

        # get meta data
        meta = self.__find_meta(dst)

        # if remote does not exist, print and return
        if meta is None:
            StdOut.display(msg=message.get(message.MISSING_FILE, location=self.name()))
            return

        if meta.get('mimeType') != self.__FOLDER_MIME:
            StdOut.display(msg=message.get(message.INVALID_FOLDER, location=self.name()))
            return

        self.__insert(src, meta)
