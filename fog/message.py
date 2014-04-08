__author__ = 'Raghav Sidhanti'

from string import Template


def get(msg, **kwargs):
    s = Template(msg)
    return s.substitute(kwargs)
