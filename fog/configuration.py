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
    GOOGLE_DRIVE_NAME = 'googledrive'
    _GOOGLE_DRIVE_HOME = ''.join([HOME, '/', GOOGLE_DRIVE_NAME])
    _GOOGLE_DRIVE_CREDENTIALS = ''.join([_GOOGLE_DRIVE_HOME, '/auth.dat'])
    _google_drive = DriveConf(
        DRIVE_NAME=GOOGLE_DRIVE_NAME,
        DRIVE_HOME=_GOOGLE_DRIVE_HOME,
        CREDENTIALS=_GOOGLE_DRIVE_CREDENTIALS
    )


    # sky drive
    SKY_DRIVE_NAME = 'skydrive'
    _SKY_DRIVE_HOME = ''.join([HOME, '/', SKY_DRIVE_NAME])
    _sky_drive = DriveConf(
        DRIVE_NAME=SKY_DRIVE_NAME,
        DRIVE_HOME=_SKY_DRIVE_HOME
    )

    # drop box
    DROP_BOX_NAME = 'dropbox'
    _DROP_BOX_HOME = ''.join([HOME, '/', DROP_BOX_NAME])
    _drop_box = DriveConf(
        DRIVE_NAME=DROP_BOX_NAME,
        DRIVE_HOME=_DROP_BOX_HOME
    )

    # available branches
    drives = {
        GOOGLE_DRIVE_NAME: _google_drive,
        SKY_DRIVE_NAME: _sky_drive,
        DROP_BOX_NAME: _drop_box
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
    def create_checkout(checkout):
        # add to checkout file
        fsutil.write(Conf.CHECKOUT, checkout)

    @staticmethod
    def remove_drive(drive_name):
        fsutil.delete(Conf.drives.get(drive_name).get(Conf.DRIVE_HOME))

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




