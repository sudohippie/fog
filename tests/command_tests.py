__author__ = 'Raghav Sidhanti'

from nose.tools import *
from fog.command import *


class TestCommandParser(object):
    _psr = None

    def setup(self):
        self._psr = CommandParser()

    # empty commands
    def test_empty(self):
        args_list = [None, [], [''], [' '], ['', ' ', '    ', '']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Unknown)

    # invalid command only
    # invalid command with arguments
    def test_invalid(self):
        args_list = [['telephone'], ['jambalaya', 'src', 'dst']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Unknown)

    # branch, no argument
    def test_branch_no_args(self):
        args_list = [['branch'], ['BRANCH'], ['bRanCH']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Branch)
            ok_(cmd.valid())

    # branch with arguments, should fail
    def test_branch_with_args(self):
        args = ['branch', 'football']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Branch)
        ok_(not cmd.valid())

    # checkout, no argument
    def test_checkout_no_args(self):
        args_list = [['checkout'], ['CHECKOUT'], ['CheCKouT']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Checkout)
            ok_(not cmd.valid())

    # checkout, with single drive name
    def test_checkout_valid_drive(self):
        args_list = [['checkout', 'googledrive']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Checkout)
            ok_(cmd.valid())

    def test_checkout_invalid_drive(self):
        args_list = [['checkout', 'mousetrap']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Checkout)
            ok_(not cmd.valid())

    # checkout, with more than one valid argument
    def test_checkout_valid_multi_args(self):
        args = ['checkout', 'googledrive', 'dropbox', 'skydrive']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Checkout)
        ok_(not cmd.valid())

    # checkout, with more than one invalid argument
    def test_checkout_valid_multi_args(self):
        args = ['checkout', 'mousetrap1', 'mousetrap2', 'mousetrap3']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Checkout)
        ok_(not cmd.valid())

    # help, no argument
    def test_help_no_args(self):
        args_list = [['help'], ['HELP'], ['heLP']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Help)
            ok_(cmd.valid())

    # help, when a single valid argument
    def test_help_valid_one_args(self):
        args = ['help', 'branch']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Help)
        ok_(cmd.valid())

    # help, single invalid arg
    def test_help_invalid_one_args(self):
        args = ['help', 'broil']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Help)
        ok_(not cmd.valid())

    # help, when multiple args
    def test_help_multi_args(self):
        args_list = [['help', 'branch', 'checkout'], ['help', 'mousetrap1', 'mousetrap2', 'mousetrap3']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Help)
            ok_(not cmd.valid())

    # init, no arguments
    def test_init(self):
        args_list = [['init'], ['INIT'], ['iNiT']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Init)
            ok_(cmd.valid())

        # init, with arguments
    def test_init_multi_args(self):
        args_list = [['init', 'branch'], ['init', 'hello', 'world']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Init)
            ok_(not cmd.valid())

    # remote, no arguments
    def test_remote(self):
        args_list = [['remote'], ['REMOTE'], ['reMOtE']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Remote)
            ok_(cmd.valid())
        # remote, with arguments

        # remote add, similar to checkout
        # remote rm, similar to checkout

        # pull, no arguments
        # pull, single arguments
        # pull, two arguments
        # pull, more than two arguments

        # push, similar to pull
        # rm, similar to pull


if __name__ == '__main__':
    test = TestCommandParser()
    test.setup()
    test.test_help_valid_one_args()