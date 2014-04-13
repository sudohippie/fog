__author__ = 'Raghav Sidhanti'

# contains all the basic local file system operations

import os
import message

from shutil import rmtree
from inout import StdIn


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


def write(path=None, data=None, prompt=False):
    if delete(path, prompt):
        f = open(abs_path(path), 'wb')
        f.write(data)
        f.close()


def delete_dirs(path=None, prompt=True):
    if exists(path):
        if prompt and not StdIn.prompt_yes(message.get(msg=message.PROMPT_OVERWRITE, file=path)):
            return False
        rmtree(abs_path(path))
    return True


def delete(path=None, prompt=False):
    if exists(path):
        if prompt and not StdIn.prompt_yes(message.get(msg=message.PROMPT_OVERWRITE, file=path)):
            return False
        os.remove(abs_path(path))
    return True


def create_dir(path=None):
    if exists(path):
        return True
    os.mkdir(abs_path(path))
    return True


def filename(path=None):
    if not path:
        return None
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)


def join_paths(path=None, file_name=None):
    if not path and not file_name:
        return None
    if not path:
        return file_name
    if not file_name:
        return path
    return os.path.join(path, file_name)


def split(path=None):
    # while path, get tail and append
    splits = []
    while path and path != '/':
        path, tail = os.path.split(path)
        if tail:
            splits.insert(0, tail)
    return splits


def is_folder(path=None):
    if exists(path):
        return os.path.isdir(path)
    return False


def list_folder(path=None):
    # todo test whether absolute paths are created
    if exists(path):
        file_names = os.listdir(abs_path(path))
        files = []
        for file_name in file_names:
            files.append(join_paths(abs_path(path), file_name))
        return files
