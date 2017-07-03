from typing import Callable, Tuple, NewType, List

import os
import re

from gitsubrepo._common import run
from gitsubrepo._git import requires_git, GIT_COMMAND, get_git_root_directory
from gitsubrepo.exceptions import UnstagedChangeException, NotAGitRepositoryException, RunException, \
    NotAGitReferenceException, NotAGitSubrepoException

_GIT_SUBREPO_COMMAND = "subrepo"
_GIT_SUBREPO_CLONE_COMMAND = "clone"
_GIT_SUBREPO_STATUS_COMMAND = "status"
_GIT_SUBREPO_PULL_COMMAND = "pull"
_GIT_SUBREPO_BRANCH_FLAG = "--branch"
_GIT_SUBREPO_VERBOSE_FLAG = "-v"
_GIT_LS_REMOTE_COMMAND = "ls-remote"

_DEFAULT_BRANCH = "master"


Branch = NewType("Branch", str)
Commit = NewType("Commit", str)
RepositoryUrl = NewType("RepositoryUrl", str)


def _get_directory_relative_to_git_root(directory: str):
    """
    TODO
    :param directory:
    :return:
    """
    return os.path.relpath(os.path.realpath(directory), get_git_root_directory(directory))


@requires_git
def requires_subrepo(func: Callable) -> Callable:
    """
    TODO
    :param func:
    :return:
    """
    def decorated(*args, **kwargs):
        try:
            run([GIT_COMMAND, _GIT_SUBREPO_COMMAND, "--version"])
        except RunException as e:
            raise RuntimeError("`git subrepo` does not appear to be working") from e
        return func(*args, **kwargs)

    return decorated


@requires_subrepo
def clone(url: str, directory: str, *, branch: str=None, tag: str=None, commit: str=None) -> Commit:
    """
    TODO
    :param url:
    :param directory:
    :param branch:
    :param tag:
    :param commit:
    :return:
    """
    if os.path.exists(directory):
        raise ValueError(f"The directory \"{directory}\" already exists")
    if branch and tag:
        raise ValueError(f"Cannot specify both branch \"{branch}\" and tag \"{tag}\"")
    if not branch and not tag and not commit:
        branch = _DEFAULT_BRANCH

    existing_parent_directory = directory
    while not os.path.exists(existing_parent_directory):
        assert existing_parent_directory != ""
        existing_parent_directory = os.path.dirname(existing_parent_directory)

    git_root = get_git_root_directory(existing_parent_directory)

    if (branch or tag) and commit:
        run([GIT_COMMAND, "fetch", url, branch if branch else tag], execution_directory=git_root)
        branch, tag = None, None
    reference = branch if branch else (tag if tag else commit)

    try:
        run([GIT_COMMAND, _GIT_SUBREPO_COMMAND, _GIT_SUBREPO_CLONE_COMMAND, _GIT_SUBREPO_VERBOSE_FLAG,
               _GIT_SUBREPO_BRANCH_FLAG, reference, url,
              os.path.relpath(directory, existing_parent_directory)],
             execution_directory=git_root)
    except RunException as e:
        if re.search("Can't clone subrepo. (Unstaged|Index has) changes", e.stderr) is not None:
            raise UnstagedChangeException(git_root) from e
        elif "Command failed:" in e.stderr:
            try:
                repo_info = run([GIT_COMMAND, _GIT_LS_REMOTE_COMMAND, url])
                if not branch and not tag and commit:
                    raise NotAGitReferenceException(
                        f"Commit \"{commit}\" no found (specify branch/tag to fetch that first if required)")
                else:
                    references = re.findall("^.+\srefs\/.+\/(.+)", repo_info, flags=re.MULTILINE)
                    if reference not in references:
                        raise NotAGitReferenceException(f"{reference} not found in {references}") from e

            except RunException as debug_e:
                if re.match("fatal: repository .* not found", debug_e.stderr):
                    raise NotAGitRepositoryException(url) from e
        raise e

    assert os.path.exists(directory)
    return status(directory)[2]


@requires_subrepo
def status(directory: str) -> Tuple[RepositoryUrl, Branch, Commit]:
    """
    TODO
    :param directory:
    :return:
    """
    if not os.path.exists(directory):
        raise ValueError(f"No subrepo found in \"{directory}\"")

    try:
        result = run([GIT_COMMAND, _GIT_SUBREPO_COMMAND, _GIT_SUBREPO_STATUS_COMMAND, _GIT_SUBREPO_VERBOSE_FLAG,
                       _get_directory_relative_to_git_root(directory)],
                      execution_directory=get_git_root_directory(directory))
    except RunException as e:
        if "Command failed: 'git rev-parse --verify HEAD'" in e.stderr:
            raise NotAGitSubrepoException(directory) from e
        raise e

    if re.search("is not a subrepo$", result):
        raise NotAGitSubrepoException(directory)

    url = re.search("Remote URL:\s*(.*)", result).group(1)
    branch = re.search("Tracking Branch:\s*(.*)", result).group(1)
    commit = re.search("Pulled Commit:\s*(.*)", result).group(1)
    return url, branch, commit


@requires_subrepo
def pull(directory: str) -> Commit:
    """
    TODO
    :param directory:
    :return:
    """
    if not os.path.exists(directory):
        raise ValueError(f"No subrepo found in \"{directory}\"")
    try:
        result = run([GIT_COMMAND, _GIT_SUBREPO_COMMAND, _GIT_SUBREPO_PULL_COMMAND, _GIT_SUBREPO_VERBOSE_FLAG,
                      _get_directory_relative_to_git_root(directory)],
                     execution_directory=get_git_root_directory(directory))
        # print(result)
    except RunException as e:
        if "Can't pull subrepo. Working tree has changes" in e.stderr:
            raise UnstagedChangeException() from e
    return status(directory)[2]


