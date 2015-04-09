"""Integration tests for git-as.
"""

import sh


from tests import base


class Simple(base.FixedPreset):
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


class NoIntersection(base.FixedPreset):

    _preset = {
        "first.section.name": "value",
        "second.section.name": "value",
    }

    def test(self):
        with self.assertRaises(sh.ErrorReturnCode):
            sh.git_as.preset("first", "second")
        self.assertGitConfigEmpty("section.name")
