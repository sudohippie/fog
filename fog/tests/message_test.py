__author__ = 'Raghav Sidhanti'

import fog.message


def string_test():
    s = fog.message.get(fog.message.MISSING_IMPLEMENTATION, drive='googledrive')
    print s


if __name__ == '__main__':
    string_test()
