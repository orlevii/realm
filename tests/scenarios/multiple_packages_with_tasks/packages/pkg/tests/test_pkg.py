import unittest

from pkg import __version__


class PkgTest(unittest.TestCase):
    def test_version(self):
        self.assertEqual(__version__, '0.1.0')
