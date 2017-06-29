from typing import Callable

from gitsubrepo._common import run
from gitsubrepo.exceptions import NotAGitRepositoryException

_GIT_COMMAND = "git"


def requires_git(func: Callable) -> Callable:
    """
    TODO
    :param func:
    :return:
    """
    def decorated(*args, **kwargs):
        try:
            run([_GIT_COMMAND, "--version"])
        except RuntimeError as e:
            raise RuntimeError("`git` does not appear to be working") from e
        return func(*args, **kwargs)

    return decorated


@requires_git
def get_git_root_directory(directory: str):
    """
    TODO
    :param directory:
    :return:
    """
    try:
        return run([_GIT_COMMAND, "rev-parse", "--show-toplevel"], directory)
    except RuntimeError as e:
        if " Not a git repository" in str(e):
            raise NotAGitRepositoryException(directory) from e

