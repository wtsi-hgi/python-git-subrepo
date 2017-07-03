
class GitsubrepoException(Exception):
    """
    TODO
    """


class UnstagedChangeException(GitsubrepoException):
    """
    TODO
    """


class NotAGitRepositoryException(GitsubrepoException):
    """
    TODO
    """


class NotAGitReferenceException(GitsubrepoException):
    """
    TODO
    """


class RunException(GitsubrepoException):
    """
    TODO
    """
    def __init__(self, stdout: str, stderr: str):
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        return f"stdout:\n{self.stdout}\n\nstderr:\n{self.stderr}"