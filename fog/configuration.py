__author__ = 'Raghav Sidhanti'


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



