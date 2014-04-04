__author__ = 'Raghav Sidhanti'
# from input argument and device - create command instance. Provides the
# necessary input arguments to command


class ArgsPrompt(object):
    @staticmethod
    def prompt(msg=''):
        _txt = [msg, ': ']
        return input(''.join(_txt))
