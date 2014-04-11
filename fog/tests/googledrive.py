__author__ = 'Raghav Sidhanti'

import httplib2
import sys
import pprint
import logging
import os

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from apiclient.http import  MediaFileUpload
from apiclient import errors

client_id = sys.argv[1]
client_secret = sys.argv[2]
scope = 'https://www.googleapis.com/auth/drive'

flow = OAuth2WebServerFlow(client_id, client_secret, scope)
logging.basicConfig()

def main():
    # 1. Check credentials validity
    storage = Storage('.googledrive/credentials.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run(flow, storage)

    # 2. Authorize http object
    http = httplib2.Http()
    http = credentials.authorize(http)

    # 3. Build drive object
    drive = build('drive', 'v2', http=http)

    # 4. Operation
    upload_file(drive, 'output.json')

    print "\nWork Complete!"

def find_file(drive, title):
    if not drive or not title:
        return None

    request = drive.files().list()
    while request:
        response = request.execute()
        items = response.get('items')

        for item in items:
            if is_same('title', title, item):
                return item

        request = drive.files().list_next(request, response)

    return None

def find_files(drive, path):
    path_list = path.split('/')
    name = None
    while not name:
        name = path_list.pop(0)

    item = find_file(drive, name)
    return _find_files_by_path_list(drive, item, path_list)

def _find_files_by_path_list(drive, item, path_list):
    # define exit condition
    if not drive or not item or not path_list or len(path_list) == 0:
        return [item]

    name = path_list.pop(0)
    # retrieve children
    response = drive.children().list(folderId=item.get('id')).execute()
    children_refs = response.get('items')

    # compare children with current dir from path
    for child_ref in children_refs:
        child_item = drive.files().get(fileId=child_ref.get('id')).execute()
        # if found, call find files by path
        if is_same('title', name, child_item):
            items = _find_files_by_path_list(drive, child_item, path_list)
            # if children exist, append node
            if items:
                items.insert(0, item)
                return items

    return None

def is_same(key, value, item):
    if item and item[key]:
        return item[key] == value
    return False

def is_folder(item):
    if item is None:
        return None

    mime = item.get('mimeType', None)
    if mime:
        return mime == 'application/vnd.google-apps.folder'
    return False

def get_file_ancestry(drive, item):
    if item is None or drive is None:
        return []
    # if no more parents
    parents = item.get('parents')
    if not parents or len(parents) == 0:
        file_ancestry = [item]
        return file_ancestry

    # retrieve the parent
    parent_id = parents[0].get('id')
    request = drive.files().get(fileId=parent_id)
    parent_item = request.execute()

    # build ancestry
    file_ancestry = get_file_ancestry(drive, parent_item)
    file_ancestry.append(item)

    return file_ancestry

def get_absolute_path(drive, item):
    pedigree = get_file_ancestry(drive, item)
    str = ''
    for file in pedigree:
        str += '/' + file.get('title')

    return str

def download_files(http, item_list):
    # preconditions
    if not http or not item_list or len(item_list) == 0:
        return

    # create cascade directories if they don't exist
    path = ''
    for i in range(0, len(item_list) - 1, 1):
        path += item_list.pop(0).get('title') + '/'

    # write the last item in the list to the directory
    item = item_list.pop(0)
    download_file(http, item, path)

def download_file(http, item, loc=''):
    if item is None:
        print "Item is None"

    # create path if necessary
    if loc and not os.path.exists(loc):
        os.makedirs(loc)

    download_url = item.get('downloadUrl', None)
    title = item['title']
    path = loc + title
    if download_url:
        resp, content = http.request(download_url)
        if resp['status'] == '200':

            if os.path.isfile(path):
                sys.stderr.write('File already exists')
            else:
                f = open(path, 'wb')
                f.write(content)
                f.close()
                print "Write to file complete. title=", title
        else:
            print "Non 200 response code for title=", title
    else:
        print "No downloadUrl for title=", title

def remote_file_exists(drive, path):
    return find_files(drive, path) is not None

def trash_file(drive, path):
    if not drive or not path:
        print 'Missing input args'
        return

    items = find_files(drive, path)
    last_item = items.pop()
    response = drive.files().trash(fileId=last_item.get('id')).execute()
    pprint.pprint(response)

def upload_file(drive, path):
    if not drive or not path:
        print 'Missing input args'
        return

    #if remote_file_exists(drive, path):
    #    print 'Remote file exists, nothing will be done'
    #    return
    media_body = MediaFileUpload(path,resumable=True)
    body ={
        'title': 'HelloWorld.txt',
        'description': 'I am not sure',
    }

    try:
        response = drive.files().insert(body=body, media_body=media_body).execute()
        pprint.pprint(response)
    except errors.HttpError, error:
        print error



if __name__ == '__main__':
  main()

