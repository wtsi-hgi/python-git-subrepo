import os
import shutil
import tarfile
import tempfile
import unittest

from git import Repo

from gitsubrepo.exceptions import NotAGitRepositoryException, NotAGitReferenceException
from gitsubrepo.subrepo import clone
from gitsubrepo.test._resources.information import TEST_TAG, TEST_TAG_COMMIT, TEST_TAG_FILE, TEST_BRANCH, \
    TEST_BRANCH_COMMIT, \
    TEST_BRANCH_FILE, TEST_COMMIT, TEST_COMMIT_BRANCH, TEST_COMMIT_FILE, TEST_COMMIT_2, TEST_COMMIT_2_BRANCH, \
    TEST_COMMIT_2_FILE, EXTERNAL_REPOSITORY_ARCHIVE, EXTERNAL_REPOSITORY_NAME

TEST_DIRECTORY_NAME = "test-directory"
TEST_GIT_REPO_DIRECTORY_NAME = "git-directory"


class TestClone(unittest.TestCase):
    """
    TODO
    """
    def setUp(self):
        self._temp_directory = tempfile.mkdtemp()

        with tarfile.open(EXTERNAL_REPOSITORY_ARCHIVE) as archive:
            archive.extractall(path=self._temp_directory)
        self._external_git_repository = os.path.join(self._temp_directory, EXTERNAL_REPOSITORY_NAME)

        self._git_directory = os.path.join(self._temp_directory, TEST_GIT_REPO_DIRECTORY_NAME)
        Repo.init(self._git_directory)

    def tearDown(self):
        shutil.rmtree(self._temp_directory)

    def test_clone_inside_non_git_directory(self):
        self.assertRaises(NotAGitRepositoryException, clone, self._external_git_repository,
                          os.path.join(self._temp_directory, TEST_DIRECTORY_NAME), tag=TEST_TAG)

    def test_clone_to_existing_directory(self):
        test_directory = os.path.join(self._temp_directory, TEST_DIRECTORY_NAME)
        os.makedirs(test_directory)
        self.assertRaises(ValueError, clone, self._external_git_repository, test_directory, tag=TEST_TAG)

    def test_clone_tag(self):
        subrepo_directory = os.path.join(self._git_directory, TEST_DIRECTORY_NAME)
        commit = clone(self._external_git_repository, subrepo_directory, tag=TEST_TAG)
        self.assertEqual(TEST_TAG_COMMIT, commit)
        self.assertTrue(os.path.exists(os.path.join(subrepo_directory, TEST_TAG_FILE)))

    def test_clone_branch(self):
        subrepo_directory = os.path.join(self._git_directory, TEST_DIRECTORY_NAME)
        commit = clone(self._external_git_repository, subrepo_directory, branch=TEST_BRANCH)
        self.assertEqual(TEST_BRANCH_COMMIT, commit)
        self.assertTrue(os.path.exists(os.path.join(subrepo_directory, TEST_BRANCH_FILE)))

    def test_clone_commit_on_master(self):
        subrepo_directory = os.path.join(self._git_directory, TEST_DIRECTORY_NAME)
        commit = clone(
            self._external_git_repository, subrepo_directory, commit=TEST_COMMIT_2, branch=TEST_COMMIT_2_BRANCH)
        self.assertEqual(TEST_COMMIT_2[0:7], commit)
        self.assertTrue(os.path.exists(os.path.join(subrepo_directory, TEST_COMMIT_2_FILE)))

    def test_clone_commit_not_on_master(self):
        subrepo_directory = os.path.join(self._git_directory, TEST_DIRECTORY_NAME)
        commit = clone(self._external_git_repository, subrepo_directory, commit=TEST_COMMIT, branch=TEST_COMMIT_BRANCH)
        self.assertEqual(TEST_COMMIT[0:7], commit)
        self.assertTrue(os.path.exists(os.path.join(subrepo_directory, TEST_COMMIT_FILE)))

    def test_clone_invalid_url(self):
        subrepo_directory = os.path.join(self._git_directory, TEST_DIRECTORY_NAME)
        self.assertRaises(NotAGitRepositoryException, clone, "http://www.example.com/", subrepo_directory)

    def test_clone_invalid_branch(self):
        subrepo_directory = os.path.join(self._git_directory, TEST_DIRECTORY_NAME)
        self.assertRaises(NotAGitReferenceException,
                          clone, self._external_git_repository, subrepo_directory, branch="non-existent")


if __name__ == "__main__":
    unittest.main()
