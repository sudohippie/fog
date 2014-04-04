__author__ = 'Raghav Sidhanti'


class ConfigError(Exception):
    def __init__(self, args):
        self.args = args
