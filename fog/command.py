__author__ = 'Raghav Sidhanti'

import os

from .io import StdIn
from .io import StdOut
from .configuration import Conf
from shutil import rmtree


# defines all the available fog commands.
# every command defines default pre and post steps.
# executes appropriate methods on services


class FogCommand(object):

    _kwargs = None

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def execute(self):
        pass


class Init(FogCommand):

    def execute(self):
        # if .fog exists, prompt user
        if os.path.exists(Conf.HOME):
            # prompt user
            resp = StdIn.prompt('This will erase current fog configurations. Would you like to continue (yes/no)?')
            if resp and resp != 'yes':
                return
            else:
                # remove .fog
                rmtree(Conf.HOME)

        # create home and files
        os.makedirs(Conf.HOME)


class Checkout(FogCommand):

    __drive = None

    def __init__(self, **kwargs):
        super(kwargs)
        self.__drive = self._kwargs['drive'].strip()
        assert self.__drive, 'Missing [drive] argument.'

    def execute(self):
        # check whether drive is valid
        for branch in Conf.BRANCHES:
            if branch == self.__drive:
                if os.path.exists(Conf.CHECKOUT):
                    os.remove(Conf.CHECKOUT)
                checkout = open(Conf.CHECKOUT, 'w')
                checkout.write(branch)
                checkout.close()
                break

        StdOut.display(msg='Invalid drive name %s', self.__drive)