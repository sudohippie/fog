__author__ = 'Raghav Sidhanti'

# contains all the basic local file system operations

import os

from shutil import rmtree


def exists(path=None):
    if path is None:
        return False
    return os.path.exists(path)


def read_line(path=None):
    line = ''
    if exists(path):
        with open(path, 'rb') as f:
            line = f.readline()

    return line


def read_lines(path=None):
    lines = ''
    if exists(path):
        with open(path, 'rb') as f:
            lines = f.readlines()

    return lines


def write(path=None, data=None):
    delete(path)

    f = open(path, 'wb')
    f.write(data)
    f.close()


def delete_dirs(path=None):
    if exists(path):
        rmtree(path)
    return True


def delete(path=None):
    if exists(path):
        os.remove(path)
    return True


def create_dir(path=None):
    if exists(path):
        return True

    os.mkdir(path)
    return True
