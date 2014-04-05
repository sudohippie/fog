__author__ = 'Raghav Sidhanti'
# from input argument and device - create command instance. Provides the
# necessary input arguments to command


class StdIn(object):
    @staticmethod
    def prompt(msg=''):
        txt = [msg, ': ']
        return raw_input(''.join(txt))


class StdOut(object):
    @staticmethod
    def display(**kwargs):
        drive = kwargs.get('drive', None)
        if not drive:
            drive = 'fog'

        msg = kwargs.get('msg', '')
        args = kwargs.get('args', '')

        txt = ''.join(['[', drive, ']', ' - ', msg])

        print txt % args
