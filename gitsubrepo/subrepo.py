from typing import Callable, Tuple, NewType

import os
import re

from gitsubrepo._git import requires_git, _GIT_COMMAND, get_git_root_directory
from gitsubrepo._common import run
from gitsubrepo.exceptions import UnstagedChangeException

_GIT_SUBREPO_COMMAND = "subrepo"
_GIT_SUBREPO_CLONE_COMMAND = "clone"
_GIT_SUBREPO_STATUS_COMMAND = "status"
_GIT_SUBREPO_PULL_COMMAND = "pull"
_GIT_SUBREPO_BRANCH_FLAG = "--branch"


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
            run([_GIT_COMMAND, _GIT_SUBREPO_COMMAND, "--version"])
        except RuntimeError as e:
            raise RuntimeError("`git subrepo` does not appear to be working") from e
        return func(*args, **kwargs)

    return decorated


@requires_subrepo
def clone(url: str, branch: str, directory: str) -> Commit:
    """
    TODO
    :param url:
    :param branch:
    :param directory:
    :return: the pulled commit
    """
    if os.path.exists(directory):
        raise ValueError(f"The directory \"{directory}\" already exists")

    existing_parent_directory = directory
    while not os.path.exists(existing_parent_directory):
        existing_parent_directory = os.path.dirname(existing_parent_directory)

    git_root = get_git_root_directory(existing_parent_directory)

    try:
        run([_GIT_COMMAND, _GIT_SUBREPO_COMMAND,
             _GIT_SUBREPO_BRANCH_FLAG, branch, _GIT_SUBREPO_CLONE_COMMAND, url,
             os.path.relpath(directory, existing_parent_directory)],
            execution_directory=git_root)
    except RuntimeError as e:
        if "Can't clone subrepo. Unstaged changes" in str(e):
            raise UnstagedChangeException(git_root) from e

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

    result = run([_GIT_COMMAND, _GIT_SUBREPO_COMMAND, _GIT_SUBREPO_STATUS_COMMAND,
                  _get_directory_relative_to_git_root(directory)],
                 execution_directory=get_git_root_directory(directory))
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
    run([_GIT_COMMAND, _GIT_SUBREPO_COMMAND, _GIT_SUBREPO_PULL_COMMAND,
         _get_directory_relative_to_git_root(directory)],
        execution_directory=get_git_root_directory(directory))
    return status(directory)[2]


