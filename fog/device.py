__author__ = 'Raghav Sidhanti'

from apiclient.discovery import build
from httplib2 import Http
from oauth2client.file import Storage
from oauth2client.tools import run
from oauth2client.client import OAuth2WebServerFlow

# define the list of devices and their behaviours


def get():
    # retrieve active drive
    # provide config and create instance
    pass


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

    pass


class GoogleDrive(Drive):
    _config = None
    _drive = None

    def __init__(self, config=None):
        self._config = config

    def open(self, **kwargs):
        storage = Storage(self._config.auth['credentials'])
        credentials = storage.get()

        # if no credentials
        if credentials is None or credentials.invalid:
            # validate credentials
            _cl_id = self._config.auth.get('client_id', None)
            _cl_sec = self._config.auth.get('client_secret', None)
            if not _cl_id or not _cl_sec:
                # TODO determine cause, notify
                print 'Missing client id and client secret'
                return False

            # run flow and store credentials
            flow = OAuth2WebServerFlow(_cl_id, _cl_sec, 'https://www.googleapis.com/auth/drive')
            credentials = run(flow, storage)

        # if every thing is good, authorize http and build drive
        http = credentials.authorize(Http())
        self._drive = build('drive', 'v2', http=http)

        if self._drive is None:
            # TODO determine cause, notify
            return False

        # TODO notify
        return True

    def close(self, **kwargs):
        self._drive = None

