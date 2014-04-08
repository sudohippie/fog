__author__ = 'Raghav Sidhanti'

import device

from inout import StdIn
from inout import StdOut
from configuration import Conf
from configuration import ConfUtil

# defines all the available fog commands.
# every command defines default pre and post steps.
# executes appropriate methods on services

_INIT_MSG = 'Already initialized. You may reinitialize by erasing existing configurations.'
_NO_CHECKOUT_MSG = 'No checkout branch. Try "%s" for usage.'
_INVALID_DRIVE_MSG = 'Invalid drive. Try "%s" for drive names or "%s" for usage.'
_ACTIVE_SIGN = '*'
_INACTIVE_SIGN = ' '
_INVALID_ARGS = 'Invalid input argument(s). Try "%s" for usage.'
_NOT_FOG_MSG = 'Not a fog directory (missing .fog). Try "%s" to initialize or "%s" for usage.'
_TRACKED_DRIVE = 'Drive %s is already tracked. Try "%s" to un-track and try again or "%s" for usage.'
_NOT_TRACKED_DRIVE = 'Drive %s is not tracked. Nothing to do here.'
_DRIVE_NOT_IMPLEMENTED = 'Unfortunately %s is not yet implemented. We are working on it and will release it soon.'


class CommandInvoker(object):
    def invoke(self, command):
        if command is not None:
            # check state
            if not ConfUtil.valid_state():
                if not isinstance(command, Help) and not isinstance(command, Init) and not isinstance(command, Invalid):
                    StdOut.display(ignore_prefix=True, msg=_NOT_FOG_MSG, args=('init', 'help'))
                    return

            command.execute()


class CommandParser(object):
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
            'branch': lambda: Branch(cmd_args),
            'checkout': lambda: Checkout(cmd_args),
            'help': lambda: Help(),
            'init': lambda: Init(cmd_args),
            'remote': lambda: Remote(cmd_args)
        }.get(cmd, lambda: Invalid(cmd_args))()


class FogCommand(object):
    _args = None

    def __init__(self, args=None):
        self._args = args

    def execute(self, **kwargs):
        pass

    def help(self):
        pass

    def valid(self):
        pass


class Init(FogCommand):

    def __reset(self):
        # if home exists, prompt user
        if ConfUtil.exists_home():
            if StdIn.prompt_yes(_INIT_MSG):
                ConfUtil.remove_home()
            else:
                return False
        return True

    def execute(self, **kwargs):
        # create home and files
        if self.__reset():
            ConfUtil.create_home()


class Checkout(FogCommand):
    def execute(self, **kwargs):

        # check whether drive is valid
        if self.__validate_args():
            drive_name = self._args[0]

            if not ConfUtil.valid_drive(drive_name):
                StdOut.display(msg=_INVALID_DRIVE_MSG, args=('branch', 'help'), ignore_prefix=True)
                return

            ConfUtil.checkout(drive_name)


    def __validate_args(self):
        if len(self._args) == 1:
            return True
        return False


class Branch(FogCommand):
    def execute(self, **kwargs):

        # read checkout file
        checkout = ConfUtil.get_checkout()

        # read branches and compare with checkout
        for name in Conf.drives.keys():
            prefix = _INACTIVE_SIGN
            if name == checkout:
                prefix = _ACTIVE_SIGN

            StdOut.display(prefix=prefix, msg=name)


class Remote(FogCommand):
    def __get_remote(self, cmd):
        return {
            '': lambda: RemoteList(self._args),
            'add': lambda: RemoteAdd(self._args),
            'rm': lambda: RemoteRm(self._args)
        }.get(cmd, lambda: Invalid(self._args))()

    def execute(self, **kwargs):
        cmd = 'invalid'

        if len(self._args) == 0:
            cmd = ''
        elif len(self._args) == 2:
            cmd = self._args[0]

        remote = self.__get_remote(cmd)
        remote.execute(**kwargs)


class RemoteList(Remote):
    def execute(self, **kwargs):
        # find all the drive config
        for name, drive in Conf.drives.items():
            prefix = _INACTIVE_SIGN
            if ConfUtil.exists_drive(name):
                prefix = _ACTIVE_SIGN
            StdOut.display(prefix=prefix, msg=name)


class RemoteAdd(FogCommand):
    def execute(self, **kwargs):
        drive_name = self._args[1]

        # reject invalid drive names
        if not ConfUtil.valid_drive(drive_name):
            StdOut.display(msg=_INVALID_DRIVE_MSG, args=('branch', 'help'), ignore_prefix=True)
            return

        # reject if already tracked
        if ConfUtil.exists_drive(drive_name):
            StdOut.display(ignore_prefix=True, msg=_TRACKED_DRIVE, args=(drive_name, 'remote rm', 'help'))
            return

        # create configs home
        ConfUtil.create_drive(drive_name)

        drive = device.get_drive(drive_name)
        if drive is not None:
            # create remote
            drive.open(**kwargs)
            drive.close(*kwargs)
        else:
            StdOut.display(ignore_prefix=True, msg=_DRIVE_NOT_IMPLEMENTED, args=drive_name)


class RemoteRm(FogCommand):
    def execute(self, **kwargs):
        drive_name = self._args[1]

        # reject invalid drive
        if not ConfUtil.valid_drive(drive_name):
            StdOut.display(msg=_INVALID_DRIVE_MSG, args=('branch', 'help'), ignore_prefix=True)
            return

        if not ConfUtil.exists_drive(drive_name):
            StdOut.display(ignore_prefix=True, msg=_NOT_TRACKED_DRIVE, args=drive_name)
            return

        ConfUtil.remove_drive(drive_name)


class Invalid(FogCommand):
    def execute(self, **kwargs):
        StdOut.display(msg=_INVALID_ARGS, args='help', ignore_prefix=True)


class Help(FogCommand):
    def execute(self, **kwargs):
        msgs = [
            'usage: fog <command> [<args>]\n\n',
            'Commonly used fog commands are:\n',
            '  branch         List available drives\n',
            '  checkout       Checkout a drive\n',
            '  init           Create an empty fog directory or reinitialize an existing one\n',
            '  pull           Download files from remote drive\n',
            '  push           Upload a file to remote drive\n',
            '  remote         List all the drives being tracked\n',
            '  remote add     Track a remote drive\n',
            '  remote rm      Un-track a remote drive\n',
            '  rm             Move a file on remote drive to trash'
        ]

        StdOut.display(msg=''.join(msgs), ignore_prefix=True)