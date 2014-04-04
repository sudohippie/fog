__author__ = 'Raghav Sidhanti'


class Conf(object):

    # standard
    HOME = '.fog'
    LOGS = ''.join([HOME, '/logs'])
    CHECKOUT = ''.join(HOME, '/checkout')

    # google
    GOOGLE_DRIVE = 'googledrive'
    GOOGLE_DRIVE_HOME = ''.join(HOME, '/', GOOGLE_DRIVE)
    GOOGLE_DRIVE_CREDENTIALS = ''.join(GOOGLE_DRIVE_HOME, '/auth.dat')

    # sky drive
    #SKY_DRIVE = 'skydrive'
    #SKY_DRIVE_HOME = ''.join(HOME, '/', SKY_DRIVE)

    # drop box
    #DROP_BOX = 'dropbox'
    #DROP_BOX_HOME = ''.join(HOME, '/', DROP_BOX)

    # available branches
    BRANCHES = [GOOGLE_DRIVE]
