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

    def parse(self, args=['invalid']):
        # clean the args
        inputs = []
        for arg in args:
            if arg:
                inputs.append(arg.strip())
        # get command object
        return self.__get_command(inputs)

    @staticmethod
    def __get_command(inputs):
        args = inputs[1:]
        # create instance for drive and return
        return {
            Branch.name(): lambda: Branch(args),
            Checkout.name(): lambda: Checkout(args),
            Help.name(): lambda: Help(inputs),
            Init.name(): lambda: Init(args),
            Remote.name(): lambda: Remote(args),
            Pull.name(): lambda: Pull(args)
        }.get(inputs[0], lambda: Invalid(args))()


class FogCommand(object):
    _args = []

    def __init__(self, args=[]):
        self._args = args

    def execute(self, **kwargs):
        pass

    def help(self):
        pass

    def valid(self):
        pass

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
            StdOut.display(msg=message.get(message.STATUS, mark=mark, drive=name))


class Remote(FogCommand):
    @staticmethod
    def name():
        return 'remote'

    def __get_remote(self, cmd):
        return {
            '': lambda: RemoteList(self._args),
            'add': lambda: RemoteAdd(self._args[1:]),
            'rm': lambda: RemoteRm(self._args[1:])
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
            StdOut.display(msg=message.get(message.STATUS, mark=mark, drive=name))


class RemoteAdd(FogCommand):

    def valid(self):
        # check argument size
        if len(self._args) != 1:
            StdOut.display(msg=message.get(message.INVALID_ARGS))
            return False

        drive_name = self._args[0]
        # reject invalid drive
        if not ConfUtil.valid_drive(drive_name):
            StdOut.display(msg=message.get(message.INVALID_DRIVE_NAME, drive=drive_name))
            return False

        # check if remote exists
        if ConfUtil.exists_drive(drive_name):
            StdOut.display(msg=message.get(message.REMOTE_EXISTS, drive=drive_name))
            return False

        return True

    def execute(self, **kwargs):
        drive_name = self._args[0]
        drive = device.get_drive(drive_name)
        if drive is not None:
            # create configs home
            ConfUtil.create_drive(drive_name)
            # create remote
            if drive.open(**kwargs):
                drive.close(**kwargs)
            else:
                # don't create home if auth fails
                ConfUtil.remove_drive(drive_name)
        else:
            StdOut.display(msg=message.get(message.MISSING_IMPLEMENTATION, drive=drive_name))


class RemoteRm(FogCommand):

    def valid(self):
        # check argument size
        if len(self._args) != 1:
            StdOut.display(msg=message.get(message.INVALID_ARGS))
            return False

        drive_name = self._args[0]
        # reject invalid drive
        if not ConfUtil.valid_drive(drive_name):
            StdOut.display(msg=message.get(message.INVALID_DRIVE_NAME, drive=drive_name))
            return False

        # check if remote exists
        if not ConfUtil.exists_drive(drive_name):
            StdOut.display(msg=message.get(message.MISSING_REMOTE, drive=drive_name))
            return False

        return True

    def execute(self, **kwargs):
        drive_name = self._args[0]
        ConfUtil.remove_drive(drive_name)


class Pull(FogCommand):
    @staticmethod
    def name():
        return 'pull'

    def valid(self):
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
        src = self._args[0]
        dst = src
        if len(self._args) == 2:
            dst = self._args[1]

        drive = device.get_active_drive()
        # open connection
        if drive.open():
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

        for idx in range(0, 2, 1):
            StdOut.display(msg=msgs[idx])

        for idx in range(2, len(msgs), 1):
            StdOut.display(template=StdOut.IND2, msg=msgs[idx])
