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
        Conf.GOOGLE_DRIVE_NAME: lambda: GoogleDrive(),
        Conf.DROP_BOX_NAME: lambda: None
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

    def __get_credentials(self):

        storage = Storage(ConfUtil.get_drive_prop(Conf.GOOGLE_DRIVE_NAME, Conf.CREDENTIALS))
        credentials = storage.get()

        # if no credentials
        if credentials is None or credentials.invalid:
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

