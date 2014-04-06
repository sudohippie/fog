__author__ = 'Raghav Sidhanti'

import fsutil
from .inout import StdIn
from .inout import StdOut
from .configuration import Conf

# defines all the available fog commands.
# every command defines default pre and post steps.
# executes appropriate methods on services

_INIT_MSG = 'This will erase fog configurations.'
_CHECKOUT_MSG = 'Invalid drive name: %s'
_ACTIVE_SIGN = '*'
_INACTIVE_SIGN = ' '


class CommandParser(object):

    _drive = None

    def __init__(self, drive):
        self._drive = drive

    def parse(self, *args):

        inputs = self.__clean(args)

        # first argument is always command
        if len(inputs) < 1:
            self.__print_missing_args()

        # second or more arguments may be needed based on command
        op = str(inputs[0]).lower()

        # create instance for drive and return
        cmd_lambda = {
            'init': lambda: Init(self._drive),
            'branch': lambda: Branch(self._drive),
            'checkout': lambda: Checkout(self._drive),
            'remote': lambda: Remote(self._drive)
        }.get(op, None)

        # if no match is found
        if cmd_lambda is None:
            self.__print_invalid_args(op)
            return None

        return cmd_lambda()

    @staticmethod
    def __clean(args):
        inputs = []
        # input should contain one or more arguments, collect the strings
        if args is not None:
            for arg in args:
                if arg:
                    inputs.append(arg)
        return inputs

    @staticmethod
    def __print_missing_args():
        _MISSING_ARGS = 'Missing one or more input argument(s). Try "help" for usage.'
        StdOut.display(msg=_MISSING_ARGS)

    @staticmethod
    def __print_invalid_args(arg):
        _INVALID_ARGS = 'Invalid input argument "%s". Try "help" for usage.'
        StdOut.display(msg=_INVALID_ARGS, args=arg)


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

        StdOut.display(msg=_CHECKOUT_MSG, args=drive_name)


class Branch(FogCommand):

    def execute(self, **kwargs):

        # read checkout file
        checkout = fsutil.read_line(Conf.CHECKOUT)

        # read branches and compare with checkout
        for name in Conf.drives.keys():
            prefix = _INACTIVE_SIGN
            if name == checkout:
                prefix = _ACTIVE_SIGN

            StdOut.display(prefix=prefix, msg=name)


class Remote(FogCommand):

    def execute(self, **kwargs):
        # find all the drive config
        for name, drive in Conf.drives.items():
            prefix = _INACTIVE_SIGN
            if fsutil.exists(drive.get(Conf.DRIVE_HOME)):
                prefix = _ACTIVE_SIGN
            StdOut.display(prefix=prefix, msg=name)
