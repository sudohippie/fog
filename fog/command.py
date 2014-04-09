__author__ = 'Raghav Sidhanti'

import device
import message

from inout import StdIn
from inout import StdOut
from configuration import Conf
from configuration import ConfUtil

# defines all the available fog commands.
# every command defines default pre and post steps.
# executes appropriate methods on services

class CommandInvoker(object):
    def invoke(self, command):

        if command is None:
            return

        # if in new state, can execute only init, help and invalid
        if not ConfUtil.exists_home():
            if not isinstance(command, Help) and not isinstance(command, Init) and not isinstance(command, Invalid):
                StdOut.display(msg=message.get(message.MISSING_HOME))
                return
        else:
            # if in ready state, all commands can be executed
            pass

        if command.valid():
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
            Branch.name(): lambda: Branch(cmd_args),
            Checkout.name(): lambda: Checkout(cmd_args),
            Help.name(): lambda: Help(),
            Init.name(): lambda: Init(cmd_args),
            Remote.name(): lambda: Remote(cmd_args),
            Pull.name(): lambda: Pull(cmd_args)
        }.get(cmd, lambda: Invalid(cmd_args))()


class FogCommand(object):
    _args = []

    def __init__(self, args=[]):
        self._args = args

    def execute(self, **kwargs):
        pass

    def help(self):
        pass

    def valid(self):
        if self._args is None:
            return False

        # clean the arguments
        strip_args = []
        for arg in self._args:
            if arg:
                strip_args.append(arg)

        self._args = strip_args

        return self._validate()

    def _validate(self):
        return True

    @staticmethod
    def name():
        pass


class Init(FogCommand):
    @staticmethod
    def name():
        return 'init'

    def __reset(self):
        # if home exists, prompt user
        if ConfUtil.exists_home():
            if StdIn.prompt_yes(message.HOME_EXISTS):
                ConfUtil.remove_home()
            else:
                return False
        return True

    def execute(self, **kwargs):
        # create home and files
        if self.__reset():
            ConfUtil.create_home()


class Checkout(FogCommand):
    @staticmethod
    def name():
        return 'checkout'

    def execute(self, **kwargs):

        # check whether drive is valid
        if self.__validate_args():
            drive_name = self._args[0]

            if not ConfUtil.valid_drive(drive_name):
                StdOut.display(msg=message.get(message.INVALID_DRIVE_NAME, drive=drive_name))
                return

            ConfUtil.checkout(drive_name)

    def __validate_args(self):
        if len(self._args) == 1:
            return True
        return False


class Branch(FogCommand):
    @staticmethod
    def name():
        return 'branch'

    def execute(self, **kwargs):

        # read checkout file
        checkout = ConfUtil.get_checkout()

        # read branches and compare with checkout
        for name in Conf.drives.keys():
            mark = message.NO
            if name == checkout:
                mark = message.YES
            StdOut.display(msg=message.get(message.STATUS, mark=mark))


class Remote(FogCommand):
    @staticmethod
    def name():
        return 'remote'

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
            mark = message.NO
            if ConfUtil.exists_drive(name):
                mark = message.YES
            StdOut.display(msg=message.get(message.STATUS, mark=mark))


class RemoteAdd(FogCommand):
    def execute(self, **kwargs):
        drive_name = self._args[1]

        # reject invalid drive names
        if not ConfUtil.valid_drive(drive_name):
            StdOut.display(msg=message.get(message.INVALID_DRIVE_NAME, drive=drive_name))
            return

        # reject if already tracked
        if ConfUtil.exists_drive(drive_name):
            StdOut.display(msg=message.get(message.REMOTE_EXISTS, drive=drive_name))
            return

        # create configs home
        ConfUtil.create_drive(drive_name)

        drive = device.get_drive(drive_name)
        if drive is not None:
            # create remote
            drive.open(**kwargs)
            drive.close(*kwargs)
        else:
            StdOut.display(msg=message.get(message.MISSING_IMPLEMENTATION, drive=drive_name))


class RemoteRm(FogCommand):
    def execute(self, **kwargs):
        drive_name = self._args[1]

        # reject invalid drive
        if not ConfUtil.valid_drive(drive_name):
            StdOut.display(msg=message.get(message.INVALID_DRIVE_NAME, drive=drive_name))
            return

        if not ConfUtil.exists_drive(drive_name):
            return

        ConfUtil.remove_drive(drive_name)


class Pull(FogCommand):
    @staticmethod
    def name():
        return 'pull'

    def _validate(self):
        if len(self._args) != 1 and len(self._args) != 2:
            return False

        # make sure drive has been checked out
        checkout = ConfUtil.get_checkout()
        if not checkout:
            StdOut.display(msg=message.get(message.MISSING_CHECKOUT))
            return False

        # make sure drive is tracked
        if not ConfUtil.exists_drive(checkout):
            StdOut.display(msg=message.get(message.MISSING_REMOTE, drive=checkout))

            return False

        return True

    def execute(self, **kwargs):
        # validate inputs
        src = self._args[0].strip()
        dst = src
        if len(self._args) == 2:
            dst = self._args[1].strip()

        drive = device.get_active_drive()
        if drive is None:
            StdOut.display(msg=message.get(message.MISSING_CHECKOUT))
            return

        # open connection
        drive.open()
        # pull
        drive.download(src=src, dst=dst)
        #close
        drive.close()


class Invalid(FogCommand):
    def execute(self, **kwargs):
        StdOut.display(msg=message.get(message.INVALID_ARGS))


class Help(FogCommand):
    @staticmethod
    def name():
        return 'help'

    def execute(self, **kwargs):
        msgs = [
            'usage: fog <command> [<args>]',
            'Commonly used fog commands are:',
            '',
            'branch         List available drives',
            'checkout       Checkout a drive',
            'init           Create an empty fog directory or reinitialize an existing one',
            'pull           Download files from remote drive',
            'push           Upload a file to remote drive',
            'remote         List all the drives being tracked',
            'remote add     Track a remote drive',
            'remote rm      Un-track a remote drive',
            'rm             Move a file on remote drive to trash'
        ]

        for idx in range(0, 3, 1):
            StdOut.display(msg=msgs[idx])

        for idx in range(3, len(msgs), 1):
            StdOut.display(template=StdOut.IND2, msgs[idx])
