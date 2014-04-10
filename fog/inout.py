__author__ = 'Raghav Sidhanti'
# from input argument and device - create command instance. Provides the
# necessary input arguments to command
import message

from string import Template


class StdIn(object):
    @staticmethod
    def prompt(msg=''):
        return raw_input(msg)

    @staticmethod
    def prompt_yes(msg=''):
        return StdIn.prompt(msg) == message.YES


class StdOut(object):
    SIMPLE = '$msg'
    IND2 = '  $msg'

    @staticmethod
    def display(template=SIMPLE, msg=''):
        t = Template(template)
        txt = t.substitute(msg=msg)
        print txt
