__author__ = 'Raghav Sidhanti'

from .configuration import ConfigError
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
    _config = None

    def __init__(self, config=None):
        self._config = config

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
    _drive = None

    def open(self, **kwargs):
        storage = Storage(self._config.drive.get['credentials', None])
        credentials = storage.get()

        # if no credentials
        if credentials is None or credentials.invalid:
            # validate credentials
            _cl_id = None
            _cl_secret = None
            # TODO Prompt for authentication

            # run flow and store credentials
            flow = OAuth2WebServerFlow(_cl_id, _cl_secret, 'https://www.googleapis.com/auth/drive')
            credentials = run(flow, storage)

        # if every thing is good, authorize http and build drive
        http = credentials.authorize(Http())
        self._drive = build('drive', 'v2', http=http)

        return True

    def close(self, **kwargs):
        self._drive = None

