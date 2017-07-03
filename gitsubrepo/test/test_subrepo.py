import unittest

import os
import shutil
import tempfile
from git import Repo

from gitsubrepo.exceptions import NotAGitRepositoryException, NotAGitReferenceException
from gitsubrepo.subrepo import clone

_TEST_REPO = "https://github.com/colin-nolan/test-repository.git"
_TEST_TAG = "1.0"
_TEST_TAG_COMMIT = "e22fcb9"
_TEST_TAG_FILE = "b.txt"
_TEST_BRANCH = "develop"
_TEST_BRANCH_COMMIT = "836d7cf"
_TEST_BRANCH_FILE = "develop.txt"
_TEST_COMMIT = "836d7cfe667fd953927a801b90e4302005e61e59"
_TEST_COMMIT_BRANCH = "develop"
_TEST_COMMIT_FILE = "develop.txt"
_TEST_COMMIT_2 = "cd682d66c4f5b9bdd5a618ecf3b8af2bf6f57f1a"
_TEST_COMMIT_2_BRANCH = "master"
_TEST_COMMIT_2_FILE = "update.txt"

_TEST_DIRECTORY_NAME = "test-directory"
_TEST_GIT_REPO_DIRECTORY_NAME = "git-directory"


class TestClone(unittest.TestCase):
    """
    TODO
    """
    def setUp(self):
        self._temp_directory = tempfile.mkdtemp()
        self._git_directory = os.path.join(self._temp_directory, _TEST_GIT_REPO_DIRECTORY_NAME)
        Repo.init(self._git_directory)

    def tearDown(self):
        shutil.rmtree(self._temp_directory)

    def test_clone_inside_non_git_directory(self):
        self.assertRaises(NotAGitRepositoryException, clone,
                          _TEST_REPO, os.path.join(self._temp_directory, _TEST_DIRECTORY_NAME), tag=_TEST_TAG)

    def test_clone_to_existing_directory(self):
        test_directory = os.path.join(self._temp_directory, _TEST_DIRECTORY_NAME)
        os.makedirs(test_directory)
        self.assertRaises(ValueError, clone, _TEST_REPO, test_directory, tag=_TEST_TAG)

    def test_clone_tag(self):
        subrepo_directory = os.path.join(self._git_directory, _TEST_DIRECTORY_NAME)
        commit = clone(_TEST_REPO, subrepo_directory, tag=_TEST_TAG)
        self.assertEqual(_TEST_TAG_COMMIT, commit)
        self.assertTrue(os.path.exists(os.path.join(subrepo_directory, _TEST_TAG_FILE)))

    def test_clone_branch(self):
        subrepo_directory = os.path.join(self._git_directory, _TEST_DIRECTORY_NAME)
        commit = clone(_TEST_REPO, subrepo_directory, branch=_TEST_BRANCH)
        self.assertEqual(_TEST_BRANCH_COMMIT, commit)
        self.assertTrue(os.path.exists(os.path.join(subrepo_directory, _TEST_BRANCH_FILE)))

    def test_clone_commit_on_master(self):
        subrepo_directory = os.path.join(self._git_directory, _TEST_DIRECTORY_NAME)
        commit = clone(_TEST_REPO, subrepo_directory, commit=_TEST_COMMIT_2, branch=_TEST_COMMIT_2_BRANCH)
        self.assertEqual(_TEST_COMMIT_2[0:7], commit)
        self.assertTrue(os.path.exists(os.path.join(subrepo_directory, _TEST_COMMIT_2_FILE)))

    def test_clone_commit_not_on_master(self):
        subrepo_directory = os.path.join(self._git_directory, _TEST_DIRECTORY_NAME)
        commit = clone(_TEST_REPO, subrepo_directory, commit=_TEST_COMMIT, branch=_TEST_COMMIT_BRANCH)
        self.assertEqual(_TEST_COMMIT[0:7], commit)
        self.assertTrue(os.path.exists(os.path.join(subrepo_directory, _TEST_COMMIT_FILE)))

    def test_clone_invalid_url(self):
        subrepo_directory = os.path.join(self._git_directory, _TEST_DIRECTORY_NAME)
        self.assertRaises(NotAGitRepositoryException, clone, "http://www.example.com/", subrepo_directory)

    def test_clone_invalid_branch(self):
        subrepo_directory = os.path.join(self._git_directory, _TEST_DIRECTORY_NAME)
        self.assertRaises(NotAGitReferenceException, clone, _TEST_REPO, subrepo_directory, branch="non-existent")


if __name__ == "__main__":
    unittest.main()
