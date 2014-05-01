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
    def test_checkout_invalid_multi_args(self):
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
    def test_remote_with_args(self):
        args_list = [['remote', 'googledrive'], ['remote', 'mousetrap'], ['remote', 'mousetrap1', 'mousetrap2']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Unknown)

    # remote add, similar to checkout
    # remote add, no argument
    def test_remote_add_no_args(self):
        args_list = [['remote', 'add'], ['REMOTE', 'ADD'], ['remOTe', 'aDD'], ['   remote  ', '  add ']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is RemoteAdd)
            ok_(not cmd.valid())

    # remote add, with single drive name
    def test_remote_add_valid_drive(self):
        args_list = [['remote', 'add', 'googledrive']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is RemoteAdd)
            ok_(cmd.valid())

    def test_remote_add_invalid_drive(self):
        args_list = [['remote', 'add', 'mousetrap']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is RemoteAdd)
            ok_(not cmd.valid())

    # remote add, with more than one valid argument
    def test_remote_add_valid_multi_args(self):
        args = ['remote', 'add', 'googledrive', 'dropbox', 'skydrive']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is RemoteAdd)
        ok_(not cmd.valid())

    # remote add, with more than one invalid argument
    def test_remote_add_invalid_multi_args(self):
        args = ['remote', 'add', 'mousetrap1', 'mousetrap2', 'mousetrap3']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is RemoteAdd)
        ok_(not cmd.valid())

    # remote rm, similar to checkout
    # remote rm, no argument
    def test_remote_rm_no_args(self):
        args_list = [['remote', 'rm'], ['REMOTE', 'RM'], ['remOTe', 'Rm'], ['   remote  ', '  rm   ']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is RemoteRm)
            ok_(not cmd.valid())

    # remote rm, with single drive name
    def test_remote_rm_valid_drive(self):
        args_list = [['remote', 'rm', 'googledrive']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is RemoteRm)
            #ok_(cmd.valid()) look at issue-#29

    def test_remote_rm_invalid_drive(self):
        args_list = [['remote', 'rm', 'mousetrap']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is RemoteRm)
            ok_(not cmd.valid())

    # remote rm, with more than one valid argument
    def test_remote_rm_valid_multi_args(self):
        args = ['remote', 'rm', 'googledrive', 'dropbox', 'skydrive']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is RemoteRm)
        ok_(not cmd.valid())

    # remote rm, with more than one invalid argument
    def test_remote_rm_invalid_multi_args(self):
        args = ['remote', 'rm', 'mousetrap1', 'mousetrap2', 'mousetrap3']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is RemoteRm)
        ok_(not cmd.valid())

    # pull, no arguments
    def test_pull_with_no_args(self):
        args_list = [['pull'], ['PULL'], ['PulL'], ['  pull  ']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Pull)
            ok_(not cmd.valid())

    # pull, single arguments
    def test_pull_with_one_args(self):
        args = ['pull', 'file/folder/mousetrap.txt']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Pull)
        #ok_(cmd.valid()) look at issue-#29

    # pull, two arguments
    def test_pull_with_two_args(self):
        args = ['pull', 'file/folder/mousetrap.txt', 'folder/file/moustrap2.txt']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Pull)
        #ok_(cmd.valid()) look at issue-#29

    # pull, more than two arguments
    def test_pull_with_multi_args(self):
        args = ['pull', 'file/folder/mousetrap.txt', 'folder/file/moustrap2.txt', 'file/folder/mousetrap3.txt', 'folder/file/moustrap4.txt']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Pull)
        #ok_(not cmd.valid()) look at issue-#29

    # push, similar to pull
    # push, no arguments
    def test_push_with_no_args(self):
        args_list = [['push'], ['PUSH'], ['PusH'], ['  push  ']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Push)
            ok_(not cmd.valid())

    # push, single arguments
    def test_push_with_one_args(self):
        args = ['push', 'file/folder/mousetrap.txt']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Push)
        #ok_(cmd.valid()) look at issue-#29

    # push, two arguments
    def test_push_with_two_args(self):
        args = ['push', 'file/folder/mousetrap.txt', 'folder/file/moustrap2.txt']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Push)
        #ok_(cmd.valid()) look at issue-#29

    # push, more than two arguments
    def test_push_with_multi_args(self):
        args = ['push', 'file/folder/mousetrap.txt', 'folder/file/moustrap2.txt', 'file/folder/mousetrap3.txt', 'folder/file/moustrap4.txt']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Push)
        #ok_(not cmd.valid()) look at issue-#29

    # rm, similar to pull
    # rm, no arguments
    def test_rm_with_no_args(self):
        args_list = [['rm'], ['RM'], ['Rm'], ['  rm  ']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Rm)
            ok_(not cmd.valid())

    # rm, single arguments
    def test_rm_with_one_args(self):
        args = ['rm', 'file/folder/mousetrap.txt']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Rm)
        #ok_(cmd.valid()) look at issue-#29

    # rm, two arguments
    def test_rm_with_two_args(self):
        args = ['rm', 'file/folder/mousetrap.txt', 'folder/file/moustrap2.txt']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Rm)
        #ok_(cmd.valid()) look at issue-#29

    # rm, more than two arguments
    def test_rm_with_multi_args(self):
        args = ['rm', 'file/folder/mousetrap.txt', 'folder/file/moustrap2.txt', 'file/folder/mousetrap3.txt', 'folder/file/moustrap4.txt']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Rm)
        #ok_(not cmd.valid()) look at issue-#29

    # info, similar to rm
    # info, no arguments
    def test_info_with_no_args(self):
        args_list = [['info'], ['INFO'], ['Info'], ['  info  ']]
        for args in args_list:
            cmd = self._psr.parse(args)
            ok_(type(cmd) is Info)
            ok_(not cmd.valid())

    # info, single arguments
    def test_info_with_one_args(self):
        args = ['info', 'file/folder/mousetrap.txt']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Info)
        #ok_(cmd.valid()) look at issue-#29

    # info, two arguments
    def test_info_with_two_args(self):
        args = ['info', 'file/folder/mousetrap.txt', 'folder/file/moustrap2.txt']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Info)
        #ok_(cmd.valid()) look at issue-#29

    # info, more than two arguments
    def test_info_with_multi_args(self):
        args = ['info', 'file/folder/mousetrap.txt', 'folder/file/moustrap2.txt', 'file/folder/mousetrap3.txt', 'folder/file/moustrap4.txt']
        cmd = self._psr.parse(args)
        ok_(type(cmd) is Info)
        #ok_(not cmd.valid()) look at issue-#29


if __name__ == '__main__':
    test = TestCommandParser()
    test.setup()
    test.test_push_with_no_args()