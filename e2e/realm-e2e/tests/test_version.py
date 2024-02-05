import unittest

from realm.utils.child_process import ChildProcess


class TestVersion(unittest.TestCase):
    def setUp(self):
        ChildProcess.FORCE_CAPTURE = True

    def test_version(self):
        out = ChildProcess.run("realm -V")
        self.assertIn("Realm", out)
