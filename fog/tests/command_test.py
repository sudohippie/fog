__author__ = 'Raghav Sidhanti'

import unittest

from fog.command import Init
from fog.command import Checkout
from fog.command import Branch
from fog.command import Remote
from fog.command import CommandParser


class CommandParserTest(unittest.TestCase):

    __parser = None

    def setUp(self):
        self.__parser = CommandParser(None)

    def test_init(self):
        cmd = self.__parser.parse('init')
        self.assertIsNotNone(cmd)

    def test_branch(self):
        cmd = self.__parser.parse('branch')
        self.assertIsNotNone(cmd)

    def test_checkout(self):
        cmd = self.__parser.parse('checkout')
        self.assertIsNotNone(cmd)

    def test_remote(self):
        cmd = self.__parser.parse('remote')
        self.assertIsNotNone(cmd)

    def test_invalid(self):
        cmd = self.__parser.parse('blah')
        self.assertIsNone(cmd)


def test_init():
    cmd = Init()
    cmd.execute()

def test_checkout():
    cmd = Checkout()
    cmd.execute(drive='googledrive')


def test_branch():
    cmd = Branch()
    cmd.execute()


def test_remote():
    cmd = Remote()
    cmd.execute()

if __name__ == '__main__':
    # test_checkout()
    # test_branch()
    # test_init()
    # test_remote()

    unittest.main()
