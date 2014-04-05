__author__ = 'Raghav Sidhanti'

from fog.command import Init
from fog.command import Checkout
from fog.command import Branch
from fog.command import Remote


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
    test_remote()
