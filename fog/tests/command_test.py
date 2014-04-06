__author__ = 'Raghav Sidhanti'

import unittest

from fog.command import Init
from fog.command import Checkout
from fog.command import Branch
from fog.command import Remote
from fog.command import Invalid
from fog.command import Help
from fog.command import CommandParser


class CommandParserTest(unittest.TestCase):

    __parser = None

    def setUp(self):
        self.__parser = CommandParser(None)

    def test_init(self):
        cmd = self.__parser.parse(['fog', 'init'])
        self.assertIsNotNone(cmd)
        self.assertTrue(type(cmd) is Init)

    def test_branch(self):
        cmd = self.__parser.parse(['fog', 'branch'])
        self.assertIsNotNone(cmd)
        self.assertTrue(type(cmd) is Branch)

    def test_checkout(self):
        cmd = self.__parser.parse(['fog', 'checkout'])
        self.assertIsNotNone(cmd)
        self.assertTrue(type(cmd) is Checkout)

    def test_remote(self):
        cmd = self.__parser.parse(['fog', 'remote'])
        self.assertIsNotNone(cmd)
        self.assertTrue(type(cmd) is Remote)

    def test_help(self):
        cmd = self.__parser.parse(['fog', 'help'])
        self.assertIsNotNone(cmd)
        self.assertTrue(type(cmd) is Help)

    def test_invalid_bad_cmd(self):
        cmd = self.__parser.parse(['fog', 'blah'])
        self.assertIsNotNone(cmd)
        self.assertTrue(type(cmd) is Invalid)

    def test_invalid_no_cmd(self):
        cmd = self.__parser.parse(['fog'])
        self.assertIsNotNone(cmd)
        self.assertTrue(type(cmd) is Invalid)

    def test_invalid_none(self):
        cmd = self.__parser.parse(None)
        self.assertIsNotNone(cmd)
        self.assertTrue(type(cmd) is Invalid)

    def test_args(self):
        cmd = self.__parser.parse(['fog', 'init', 'src', 'dest'])
        self.assertIsNotNone(cmd)
        self.assertTrue(type(cmd) is Init)


def test_init():
    cmd = Init()
    cmd.execute()


def test_checkout():
    cmd = Checkout(args=['dropbox'])
    cmd.execute()


def test_branch():
    cmd = Branch()
    cmd.execute()


def test_remote():
    cmd = Remote()
    cmd.execute()


def test_help():
    cmd = Help()
    cmd.execute()

if __name__ == '__main__':
    test_checkout()
    test_branch()
    test_init()
    test_remote()
    test_help()

    unittest.main()
