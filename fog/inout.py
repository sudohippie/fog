__author__ = 'Raghav Sidhanti'
# from input argument and device - create command instance. Provides the
# necessary input arguments to command


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
    @staticmethod
    def display(**kwargs):
        prefix = kwargs.get('prefix', None)
        ignore_prefix = kwargs.get('ignore_prefix', False)
        msg = kwargs.get('msg', '')
        args = kwargs.get('args', None)

        if prefix is None:
            prefix = 'fog'

        txt_list = []

        if not ignore_prefix:
            txt_list.append('[')
            txt_list.append(prefix)
            txt_list.append(']')
            txt_list.append(' ')

        txt_list.append(msg)

        txt = ''.join(txt_list)

        if args is None:
            print txt
        else:
            print txt % args

