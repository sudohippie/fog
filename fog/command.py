__author__ = 'Raghav Sidhanti'

import os

from inout import StdIn
from inout import StdOut
from configuration import Conf
from shutil import rmtree


# defines all the available fog commands.
# every command defines default pre and post steps.
# executes appropriate methods on services


class FogCommand(object):

    _drive = None

    def __init__(self, drive=None):
        self._drive = drive

    def execute(self, **kwargs):
        pass


class Init(FogCommand):

    def __clean(self):
        # if home exists, prompt user
        if os.path.exists(Conf.HOME):
            resp = StdIn.prompt('This will erase current fog configurations. Would you like to continue (yes/no)?')
            if resp == 'yes':
                rmtree(Conf.HOME)
            else:
                return False
        return True

    def execute(self, **kwargs):
        # create home and files
        if self.__clean():
            os.makedirs(Conf.HOME)


class Checkout(FogCommand):

    def execute(self, **kwargs):

        drive_name = kwargs.get('drive', '')

        # check whether drive is valid
        for branch in Conf.BRANCHES:
            if branch == drive_name:
                if os.path.exists(Conf.CHECKOUT):
                    os.remove(Conf.CHECKOUT)
                checkout = open(Conf.CHECKOUT, 'w')
                checkout.write(branch)
                checkout.close()
                break

        StdOut.display(msg='Invalid drive: %s', args=drive_name)