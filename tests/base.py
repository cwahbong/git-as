"""Base classes for test cases."""

import os
import tempfile
import unittest

import sh


class GitTest(unittest.TestCase):
    """Test case that needs a git repository.
    """

    @classmethod
    def setUpClass(cls):
        """Prepare a temporaty directory for repositories needed by test case.
        """
        cls._dir_root = tempfile.TemporaryDirectory(prefix=cls.__name__)

    @classmethod
    def tearDownClass(cls):
        cls._dir_root.cleanup()

    def setUp(self):
        self._old_cwd = os.getcwd()
        self._dir_repo = tempfile.TemporaryDirectory(dir=self._dir_root.name)
        sh.git.init(self._dir_repo.name)
        os.chdir(self._dir_repo.name)

    def tearDown(self):
        os.chdir(self._old_cwd)
        self._dir_repo.cleanup()

    def assertGitConfigEqual(self, name, value):
        """Checks that git local config name has that value."""
        self.assertEqual(sh.git.config("--null", "--local", "--get", name), value + "\0")

    def assertGitConfigEmpty(self, name):
        """Checks that git local config name has no value."""
        with self.assertRaises(sh.ErrorReturnCode_1, msg="Should be empty"):
            sh.git.config("--null", "--local", "--get", name)


class FixedPreset(GitTest):
    """Test case with predefined presets.

    Subclass instances could set _preset by themselves.
    """
    _preset = {}

    def setUp(self):
        super().setUp()
        for name, value in self._preset.items():
            sh.git.config("--local", "as.preset.{}".format(name), value)
