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
        prefix = kwargs.get('prefix', None)
        if not prefix:
            prefix = 'fog'

        msg = kwargs.get('msg', '')
        args = kwargs.get('args', None)

        txt = ''.join(['[', prefix, ']', ' ', msg])

        if args is None:
            print txt
        else:
            print txt % args

