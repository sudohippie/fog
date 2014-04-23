__author__ = 'Raghav Sidhanti'

from nose.tools import *
from fog.message import *


def setup():
    pass


def teardown():
    pass


def test_message_no_ph():
    # when no placeholders
    s = 'hello, world'
    assert_equals(get(msg=s), s)


def test_message_help_ph():
    # when help placeholder
    s = '$help'
    assert_not_equals(get(msg=s), s)


def test_message_yes_ph():
    # when yes placeholder
    s = '$yes'
    assert_not_equals(get(msg=s), s)


def test_message_continue_ph():
    # when continue placeholder
    s = '$continue'
    assert_not_equals(get(msg=s), s)


def test_message_custom_ph():
    # when custom placeholder
    s = 'hello, $txt'
    assert_equals(get(msg=s, txt='world'), 'hello, world')


@raises(Exception)
def test_message_missing_ph():
    # when custom placeholder no data
    s = 'hello, $txt'
    assert_equals(get(msg=s), s)
