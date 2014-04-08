__author__ = 'Raghav Sidhanti'

import fog.message


def string_test():
    s = fog.message.get('$who, world', who='hello')
    print s


if __name__ == '__main__':
    string_test()
