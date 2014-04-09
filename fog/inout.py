__author__ = 'Raghav Sidhanti'
# from input argument and device - create command instance. Provides the
# necessary input arguments to command
from string import Template


class StdIn(object):
    @staticmethod
    def prompt(msg=''):
        txt = [msg, ': ']
        return raw_input(''.join(txt))

    @staticmethod
    def prompt_yes(msg=''):
        txt = [msg,
               '\n',
               'Would you like to continue (yes/no)?']
        resp = StdIn.prompt(''.join(txt))
        return resp == 'yes'


class StdOut(object):
    SIMPLE = '$msg'
    IND2 = '  $msg'

    @staticmethod
    def display(template=SIMPLE, msg=''):
        t = Template(template)
        txt = t.substitute(msg=msg)
        print txt
