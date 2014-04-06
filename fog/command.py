__author__ = 'Raghav Sidhanti'

import fsutil
from inout import StdIn
from inout import StdOut
from configuration import Conf

# defines all the available fog commands.
# every command defines default pre and post steps.
# executes appropriate methods on services

_INIT_MSG = 'This will erase fog configurations.'
_CHECKOUT_MSG = 'Invalid drive name'
_ACTIVE_SIGN = '*'
_INACTIVE_SIGN = ' '
_INVALID_ARGS = 'Invalid input argument(s). Try "help" for usage.'


class CommandInvoker(object):

    def invoke(self, command):
        if command is not None:
            command.execute()


class CommandParser(object):

    _drive = None

    def __init__(self, drive):
        self._drive = drive

    def parse(self, args):
        inputs = self.__clean(args)

        cmd = str(inputs[0]).lower()
        cmd_args = []
        for idx in range(1, len(inputs), 1):
            cmd_args.append(args[idx])

        return self.__get_command(cmd, cmd_args)

    def __clean(self, args):
        inputs = []

        if args is None or len(args) == 1:
            inputs.append('invalid')
            return inputs

        # remote fog command
        args.pop(0)

        # clean multiple spaces
        if args is not None:
            for arg in args:
                if arg:
                    inputs.append(arg.strip())

        return inputs

    def __get_command(self, cmd='', cmd_args=[]):
        # create instance for drive and return
        return {
            'branch': lambda: Branch(self._drive, cmd_args),
            'checkout': lambda: Checkout(self._drive, cmd_args),
            'help': lambda: Help(),
            'init': lambda: Init(self._drive, cmd_args),
            'remote': lambda: Remote(self._drive, cmd_args)
        }.get(cmd, lambda: Invalid())()


class FogCommand(object):

    _drive = None
    _args = None

    def __init__(self, drive=None, args=None):
        self._args = args
        self._drive = drive

    def execute(self, **kwargs):
        pass

    def _validate_args(self):
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

        # check whether drive is valid
        if self._validate_args():
            drive_name = self._args[0]

            for name in Conf.drives.keys():
                if name == drive_name:
                    fsutil.delete(Conf.CHECKOUT)
                    fsutil.write(Conf.CHECKOUT, name)
                    return

        StdOut.display(msg=_CHECKOUT_MSG, ignore_prefix=True)

    def _validate_args(self):
        if len(self._args) == 1:
            return True
        return False


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


class Invalid(FogCommand):

    def execute(self, **kwargs):
        StdOut.display(msg=_INVALID_ARGS, ignore_prefix=True)


class Help(FogCommand):

    def execute(self, **kwargs):
        msgs = [
            'usage: fog <command> [<args>]\n\n',
            'Commonly used fog commands are:\n',
            '\tbranch         List available drives\n',
            '\tcheckout       Checkout a drive\n',
            '\tinit           Create an empty fog directory or reinitialize an existing one\n',
            '\tpull           Download files from remote drive\n',
            '\tpush           Upload a file to remote drive\n',
            '\tremote         List all the drives being tracked\n',
            '\tremote add     Track a remote drive\n',
            '\tremote rm      Un-track a remote drive\n',
            '\trm             Move a file on remote drive to trash'
        ]

        StdOut.display(msg=''.join(msgs), ignore_prefix=True)
