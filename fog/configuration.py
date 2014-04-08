__author__ = 'Raghav Sidhanti'

import fsutil


class DriveConf(object):
    kw = None

    def __init__(self, **kwargs):
        self.kw = kwargs

    def get(self, key=''):
        return self.kw.get(key)


class Conf(object):
    # standard
    HOME = '.fog'
    LOGS = ''.join([HOME, '/logs'])
    CHECKOUT = ''.join([HOME, '/checkout'])

    DRIVE_NAME = 'DRIVE_NAME'
    DRIVE_HOME = 'DRIVE_HOME'
    CREDENTIALS = 'CREDENTIALS'

    # google
    GOOGLE = 'googledrive'
    _GOOGLE_HOME = ''.join([HOME, '/', GOOGLE])
    _GOOGLE_CREDENTIALS = ''.join([_GOOGLE_HOME, '/auth.dat'])
    _google = DriveConf(
        DRIVE_NAME=GOOGLE,
        DRIVE_HOME=_GOOGLE_HOME,
        CREDENTIALS=_GOOGLE_CREDENTIALS
    )


    # sky drive
    MS = 'skydrive'
    _MS_HOME = ''.join([HOME, '/', MS])
    _ms = DriveConf(
        DRIVE_NAME=MS,
        DRIVE_HOME=_MS_HOME
    )

    # drop box
    DB = 'dropbox'
    _DB_HOME = ''.join([HOME, '/', DB])
    _db = DriveConf(
        DRIVE_NAME=DB,
        DRIVE_HOME=_DB_HOME
    )

    # available branches
    drives = {
        GOOGLE: _google,
        MS: _ms,
        DB: _db
    }


class ConfUtil(object):
    # checks whether the given branch is valid
    @staticmethod
    def valid_drive(branch):
        # search in static branches
        for k in Conf.drives.keys():
            if k == branch:
                return True
        return False

    @staticmethod
    def valid_state():
        # check for whether there are any anomalies with the configurations
        return fsutil.exists(Conf.HOME)

    @staticmethod
    def get_checkout():
        # read file, spit out result
        return fsutil.read_line(Conf.CHECKOUT)

    @staticmethod
    def checkout(checkout):
        # add to checkout file
        fsutil.write(Conf.CHECKOUT, checkout)

    @staticmethod
    def remove_drive(drive_name):
        fsutil.delete_dirs(Conf.drives.get(drive_name).get(Conf.DRIVE_HOME))

    @staticmethod
    def remove_home():
        fsutil.delete_dirs(Conf.HOME)

    @staticmethod
    def create_home():
        fsutil.create_dir(Conf.HOME)

    @staticmethod
    def create_drive(drive_name):
        fsutil.create_dir(Conf.drives.get(drive_name).get(Conf.DRIVE_HOME))

    @staticmethod
    def exists_drive(drive_name):
        return fsutil.exists(Conf.drives.get(drive_name).get(Conf.DRIVE_HOME))

    @staticmethod
    def exists_home():
        return fsutil.exists(Conf.HOME)

    @staticmethod
    def get_drive_prop(drive_name, prop_name):
        drive = Conf.drives.get(drive_name, None)

        if drive is None:
            return ''

        return drive.get(prop_name)




