__author__ = 'Raghav Sidhanti'

import fsutil
from .inout import StdIn
from .inout import StdOut
from .configuration import Conf

# defines all the available fog commands.
# every command defines default pre and post steps.
# executes appropriate methods on services

_INIT_MSG = 'This will erase fog configurations.'


class FogCommand(object):

    _drive = None

    def __init__(self, drive=None):
        self._drive = drive

    def execute(self, **kwargs):
        pass


class Init(FogCommand):

    def __clean(self):
        # if home exists, prompt user
        if fsutil.exists(Conf.HOME):
            if StdIn.prompt_yes(_INIT_MSG):
                fsutil.delete_dirs(Conf.HOME)
            else:
                return False
        return True

    def execute(self, **kwargs):
        # create home and files
        if self.__clean():
            fsutil.create_dir(Conf.HOME)


class Checkout(FogCommand):

    def execute(self, **kwargs):

        drive_name = kwargs.get('drive', '')

        # check whether drive is valid
        for name in Conf.drives.keys():
            if name == drive_name:
                fsutil.delete(Conf.CHECKOUT)
                fsutil.write(Conf.CHECKOUT, name)
                return

        StdOut.display(msg='Unknown drive: %s', args=drive_name)


class Branch(FogCommand):

    def execute(self, **kwargs):

        # read checkout file
        checkout = fsutil.read_line(Conf.CHECKOUT)

        # read branches and compare with checkout
        for name in Conf.drives.keys():
            prefix = ' '
            if name == checkout:
                prefix = '*'

            StdOut.display(prefix=prefix, msg=name)


class Remote(FogCommand):

    def execute(self, **kwargs):
        # find all the drive config
        for name, drive in Conf.drives.items():
            prefix = ' '
            if fsutil.exists(drive.get(Conf.DRIVE_HOME)):
                prefix = '*'
            StdOut.display(prefix=prefix, msg=name)
