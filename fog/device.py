__author__ = 'Raghav Sidhanti'

from fog.inout import StdIn
from fog.configuration import Conf

from apiclient.discovery import build
from httplib2 import Http
from oauth2client.file import Storage
from oauth2client.tools import run
from oauth2client.client import OAuth2WebServerFlow

# define the list of devices and their behaviours


def get():
    # get configs
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


class GoogleDrive(Drive):
    __drive = None

    def __get_credentials(self):

        storage = Storage(Conf.GOOGLE_DRIVE_CREDENTIALS)
        credentials = storage.get()

        # if no credentials
        if credentials is None or credentials.invalid:
            # validate credentials
            id = StdIn.prompt('Enter Google client id')
            secret = StdIn.prompt('Enter Google client secret')

            if not id or not secret:
                return None

            # run flow and store credentials
            flow = OAuth2WebServerFlow(id, secret, 'https://www.googleapis.com/auth/drive')
            credentials = run(flow, storage)

        return credentials

    def open(self, **kwargs):

        credentials = self.__get_credentials()

        if credentials is not None:
            # if every thing is good, authorize http and build drive
            http = credentials.authorize(Http())
            self.__drive = build('drive', 'v2', http=http)
            return True

        return False

    def close(self, **kwargs):
        self.__drive = None

