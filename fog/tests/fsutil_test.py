__author__ = 'Raghav Sidhanti'

import fog.fsutil
import unittest


class FsUtilTest(unittest.TestCase):

    # Test absolute path
    def test_absolute(self):
        path = '/var/logs'

        abspath = fog.fsutil.abs_path(path)
        self.assertIsNotNone(abspath)
        self.assertEqual(path, abspath)

    # test . path
    def test_current(self):
        path = '.'

        abspath = fog.fsutil.abs_path(path)
        self.assertIsNotNone(abspath)
        self.assertIsNot(path, abspath)
        self.assertTrue(path not in abspath)

    def test_relative_current(self):
        path = './undefined0/undefined1'

        abspath = fog.fsutil.abs_path(path)
        self.assertIsNotNone(abspath)
        self.assertIsNot(path, abspath)
        self.assertTrue('.' not in abspath)

    # test ~ path
    def test_home(self):
        path = '~'

        abspath = fog.fsutil.abs_path(path)
        self.assertIsNotNone(abspath)
        self.assertIsNot(path, abspath)
        self.assertTrue(path not in abspath)

    def test_relative_home(self):

        path = '~/undefined0/undefined1'

        abspath = fog.fsutil.abs_path(path)
        self.assertIsNotNone(abspath)
        self.assertIsNot(path, abspath)
        self.assertTrue('~' not in abspath)

    # test .. path
    def test_parent(self):
        path = '../'

        abspath = fog.fsutil.abs_path(path)
        self.assertIsNotNone(abspath)
        self.assertIsNot(path, abspath)
        self.assertTrue(path not in abspath)

    def test_relative_parent(self):
        path = '../../undefined0/undefined1'

        abspath = fog.fsutil.abs_path(path)
        self.assertIsNotNone(abspath)
        self.assertIsNot(path, abspath)
        self.assertTrue('..' not in abspath)

    def test_split0(self):
        path = 'hell/hel'

        r = fog.fsutil.split(path)

        self.assertIsNotNone(r)
        self.assertEqual(2, len(r))
        self.assertEqual('hell', r[0])
        self.assertEqual('hel', r[1])

    def test_split1(self):
        path = '/hell/hel'

        r = fog.fsutil.split(path)

        self.assertIsNotNone(r)
        self.assertEqual(2, len(r))
        self.assertEqual('hell', r[0])
        self.assertEqual('hel', r[1])

    def test_split2(self):
        path = '/'

        r = fog.fsutil.split(path)

        self.assertIsNotNone(r)
        self.assertEqual(0, len(r))

    def test_split3(self):
        path = 'hel'

        r = fog.fsutil.split(path)

        self.assertIsNotNone(r)
        self.assertEqual(1, len(r))
        self.assertEqual('hel', r[0])

    def test_split3(self):
        path = None

        r = fog.fsutil.split(path)

        self.assertIsNotNone(r)
        self.assertEqual(0, len(r))

if __name__ == '__main__':
    unittest.main()


