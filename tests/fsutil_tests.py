__author__ = 'Raghav Sidhanti'

from nose.tools import *
from fog.fsutil import *


def setup():
    pass


def teardown():
    pass


# UNIX platform
def test_unix_abspath_empty():
    eq_(abs_path(None), None)
    eq_(abs_path(''), None)


def test_unix_abspath_absolute():
    eq_(abs_path('/tmp/test/logs'), '/tmp/test/logs')


def test_unix_abspath_relative():
    relative_paths = ['.', './test', '../', '~', '~/test', 'test']
    for path in relative_paths:
        ok_(abs_path(path))
        ok_(abs_path(path) != path)
        ok_(abs_path(path).startswith('/'), 'absolute path for ' + path + ' does not start with /')


def test_unix_join_empty():
    empty = [None, '']
    for e1 in empty:
        for e2 in empty:
            ok_(join_paths(e1, e2) is None, 'Non-None value returned for empty input')

    for e in empty:
        eq_(join_paths('/test/folder', e), '/test/folder', 'Join not equal to path when filename is empty')

    for idx in range(0, len(empty), 1):
        eq_(join_paths(empty[idx], 'text.txt'), 'text.txt', 'Join not equal to filename when path is empty')


def test_unix_join_paths():
    eq_(join_paths('/test/path', '/another/path'), '/another/path')
    eq_(join_paths('/test/path/', 'another/path'), '/test/path/another/path')
    eq_(join_paths('/test/path/', '/another/path'), '/another/path')


def test_unix_join_file():
    paths = ['/test/path', 'test/path', '.', './test/path', '../test/path', '~', '~/test/path']
    for path in paths:
        ok_(join_paths(path, 'file.txt'))
        ok_(join_paths(path, 'file.txt') != 'file.txt')
        ok_(join_paths(path, 'file.txt').endswith('file.txt'), 'join path does not end with file name')


def test_unix_split_empty():
    empty = [None, '', '/']
    for e in empty:
        eq_(len(split(e)), 0, 'path is splittable = %s' % e)


def test_unix_split_relative_paths():
    relatives = ['.', '../', '../test/folder' '~', '~/test/folder', 'folder']
    for r in relatives:
        ok_(len(split(r)) > 0, 'path is empty for relative path = %s' % r)


def test_unix_split_absolute_paths():
    absolutes = ['/test/folder', '/test/folders/']
    for a in absolutes:
        eq_(len(split(a)), 2, 'absolute path is not split correctly for path = %s' % a)


def test_unix_split_invalid_slash_count():
    invalids = ['///test/folder', '/test///folder', '/test/folder///']
    for i in invalids:
        eq_(len(split(i)), 2, 'incorrect number of splits for invalid path = %s' % i)


def test_unix_filename_empty():
    empty = ['', None]
    for e in empty:
        eq_(filename(e), None)

    ok_(not filename('/'))


def test_unix_filename_file():
    path = ['./text.txt', './folder/text.txt', '../text.txt', '../folder/text.txt', '~/text.txt', '~/folder/text.txt',
            'text.txt', '/tmp/folder/text.txt']
    for p in path:
        eq_(filename(p), 'text.txt', 'Filename was not extracted from relative path = %s' % p)


def test_unix_filename_folder():
    path = ['./folder/', './paretn/folder/', '../folder/', '../parent/folder/', '~/folder/', '~/folder/folder/',
            'folder/', '/tmp/parent/folder/']
    for p in path:
        eq_(filename(p), 'folder', 'Folder name was not extracted from relative path = %s' % p)

# Windows platform

