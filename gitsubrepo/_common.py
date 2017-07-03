import subprocess
from typing import List

from gitsubrepo.exceptions import RunException

_DATA_ENCODING = "utf-8"
_SUCCESS_RETURN_CODE = 0


def run(arguments: List[str], execution_directory: str=None) -> str:
    """
    TODO
    :param arguments:
    :return:
    """
    process = subprocess.Popen(
        arguments, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, cwd=execution_directory)
    out, error = process.communicate()
    stdout = out.decode(_DATA_ENCODING).rstrip()
    if process.returncode == _SUCCESS_RETURN_CODE:
        return stdout
    else:
        raise RunException(stdout, error.decode(_DATA_ENCODING).rstrip())
