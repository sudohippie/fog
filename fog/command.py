__author__ = 'Raghav Sidhanti'

from inout import StdIn
from inout import StdOut
from configuration import Conf
from configuration import ConfUtil

# defines all the available fog commands.
# every command defines default pre and post steps.
# executes appropriate methods on services

_INIT_MSG = 'This will erase fog configurations.'
_CHECKOUT_MSG = 'Invalid drive. Try "%s" for drive names or "%s" for usage.'
_ACTIVE_SIGN = '*'
_INACTIVE_SIGN = ' '
_INVALID_ARGS = 'Invalid input argument(s). Try "%s" for usage.'
_NOT_FOG_MSG = 'Not a fog directory (missing .fog). Try "%s" for usage.'


class CommandInvoker(object):

    def invoke(self, command):
        if command is not None:
            # check state
            if not ConfUtil.is_valid_state():
                if not isinstance(command, Help) and not isinstance(command, Init) and not isinstance(command, Invalid):
                    StdOut.display(ignore_prefix=True, msg=_NOT_FOG_MSG, args='help')
                    return

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

    def help(self):
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

            for name in Conf.drives.keys():
                if name == drive_name:
                    ConfUtil.create_checkout(name)
                    return

        StdOut.display(msg=_CHECKOUT_MSG, args=('branch', 'help'), ignore_prefix=True)

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

    def execute(self, **kwargs):
        # find all the drive config
        for name, drive in Conf.drives.items():
            prefix = _INACTIVE_SIGN
            if ConfUtil.exists_drive(name):
                prefix = _ACTIVE_SIGN
            StdOut.display(prefix=prefix, msg=name)


class RemoteAdd(FogCommand):

    def execute(self, **kwargs):
        pass


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
