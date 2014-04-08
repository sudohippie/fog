__author__ = 'Raghav Sidhanti'

from inout import StdIn
from inout import StdOut
from configuration import Conf
from configuration import ConfUtil

from apiclient.discovery import build
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
        Conf.GOOGLE: lambda: GoogleDrive(),
        Conf.DB: lambda: None
    }.get(name, lambda: None)()


class Drive(object):
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

    def __get_credentials(self):

        storage = Storage(ConfUtil.get_drive_prop(Conf.GOOGLE, Conf.CREDENTIALS))
        credentials = storage.get()

        # if no credentials
        if credentials is None or credentials.invalid:
            StdOut.display(ignore_prefix=True, msg='Google credentials are missing or may have been updated.')
            # validate credentials
            id = StdIn.prompt('Enter Google client id')
            secret = StdIn.prompt('Enter Google client secret')

            if not id or not secret:
                return None

            StdOut.display(ignore_prefix=True,
                           msg='Google requires your consent. Check your default browser to accept access privileges.')
            # run flow and store credentials
            flow = OAuth2WebServerFlow(id, secret, 'https://www.googleapis.com/auth/drive')
            credentials = run(flow, storage)

        return credentials

    def __find_meta(self, title):
        # preconditions
        if not title:
            # todo missing file name for meta download
            return

        # download meta until file is found
        req = self.__drive.files().list()
        while req:
            resp = req.execute()
            metas = resp.get('items')
            for meta in metas:
                if metas.get('title') == title:
                    return meta
            # paginate
            req = self.__drive.files().list_next(req, resp)

        return None

    def __find_child_metas(self, meta, titles):
        # exit condition, if title is len == 0 return meta
        if titles is None or len(titles) == 0:
            return []
        if meta is None:
            return None

        title = titles.pop(0)

        # get children for meta
        resp = self.__drive.children().list(folderId=meta.get('id')).execute()
        children = resp.get('items')

        # search for title amongst children
        for child in children:
            child_meta = self.__drive.files().get(fileId=child.get('id')).execute()
            # if found, save meta and title, recurs
            if child_meta is not None and child_meta.get('title') == title:
                child_metas = self.__find_child_metas(child_meta, titles)
                if child_metas:
                    # add in-front of the list
                    child_metas.insert(0, child_meta)
                    return child_metas
        return None

    def __get_download_url(self, path):
        # preconditions
        if not path:
            # todo log empty path
            return

        # split the input path
        titles = path.split('/')
        # retrieve meta for first item,
        root_meta = self.__find_meta(titles.pop(0).strip())
        # get metas for its children
        child_metas = self.__find_child_metas(root_meta, titles)

        metas = []
        if root_meta:
            metas.append(root_meta)
        if child_metas:
            metas.append(child_metas)

        if len(metas) > 0:
            last_meta = metas.pop(len(metas) - 1)
            return last_meta.get('downloadUrl', None)
        return None

    def __get_content(self, url):
        if not url:
            return None

        resp, content = self.__http.request(url)

        if resp.get('status') != 200:
            # todo log un successful request
            return None

        return content

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
        # preconditions, check drive state
        if self.__drive is None:
            # todo log unauthenticated drive
            return

        src = kwargs.get('src', None)
        if not src:
            # todo log missing src
            return

        # get download url for file path
        url = self.__get_download_url(src)
        # download content
        return self.__get_content(url)
