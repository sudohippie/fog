__author__ = 'Raghav Sidhanti'

# contains all the basic local file system operations

import os

from shutil import rmtree


def abs_path(path=None):
    if path is None:
        return None

    exp_home = os.path.expanduser(path)
    real_path = os.path.abspath(exp_home)
    return os.path.abspath(real_path)


def exists(path=None):
    if path is None:
        return False
    return os.path.exists(abs_path(path))


def read_line(path=None):
    line = ''
    if exists(path):
        with open(abs_path(path), 'rb') as f:
            line = f.readline()
    return line


def read_lines(path=None):
    lines = ''
    if exists(path):
        with open(abs_path(path), 'rb') as f:
            lines = f.readlines()
    return lines


def write(path=None, data=None):
    if delete(path):
        f = open(abs_path(path), 'wb')
        f.write(data)
        f.close()


def delete_dirs(path=None):
    if exists(path):
        rmtree(abs_path(path))
    return True


def delete(path=None):
    if exists(path):
        os.remove(abs_path(path))
    return True


def create_dir(path=None):
    if exists(path):
        return True
    os.mkdir(abs_path(path))
    return True
