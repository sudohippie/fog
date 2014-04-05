__author__ = 'Raghav Sidhanti'
# from input argument and device - create command instance. Provides the
# necessary input arguments to command


class StdIn(object):
    @staticmethod
    def prompt(msg=''):
        txt = [msg, ': ']
        return input(''.join(txt))


class StdOut(object):
    @staticmethod
    def display(drive='fog', msg='', *args):
        txt = ['[', drive, ']', ' - ', msg]
        print ''.join(txt) % args
