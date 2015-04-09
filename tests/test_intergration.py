"""Integration tests for git-as.
"""
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


class Simple(FixedPreset):
    """Test case with a preset with only one key-value.
    """
    _preset = {
        "simpletest.section.abcd": "dbca"
    }

    def test_apply(self):
        sh.git_as.preset("simpletest")
        self.assertGitConfigEqual("section.abcd", "dbca")

    def test_clear_by_name(self):
        sh.git_as.preset("simpletest")
        sh.git_as.clear("simpletest")
        self.assertGitConfigEmpty("as.applied.simpletest")
        self.assertGitConfigEmpty("section.abcd")

    def test_clear_all(self):
        sh.git_as.preset("simpletest")
        sh.git_as.clear("--all")
        self.assertGitConfigEmpty("as.applied.simpletest")
        self.assertGitConfigEmpty("section.abcd")


class NoIntersection(FixedPreset):

    _preset = {
        "first.section.name": "value",
        "second.section.name": "value",
    }

    def test(self):
        with self.assertRaises(sh.ErrorReturnCode):
            sh.git_as.preset("first", "second")
        self.assertGitConfigEmpty("section.name")
