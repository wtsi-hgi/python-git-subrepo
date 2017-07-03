
class GitsubrepoException(Exception):
    """
    Base class for all exceptions within this library.
    """


class UnstagedChangeException(GitsubrepoException):
    """
    Raised when there are unexpected unchanged changes to a repository.
    """


class NotAGitRepositoryException(GitsubrepoException):
    """
    Raised when a Git repository was expected but not given.
    """


class NotAGitReferenceException(GitsubrepoException):
    """
    Raised when a Git reference was expected but not given.
    """


class NotAGitSubrepoException(GitsubrepoException):
    """
    Raised when a Git subrepo was expected but not given.
    """


class RunException(GitsubrepoException):
    """
    Raised when a run exited with a non-zero exit code.
    """
    def __init__(self, stdout: str, stderr: str):
        """
        Constructor.
        :param stdout: what the executable wrote to stdout
        :param stderr: what the executable wrote to stderr
        """
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        return f"stdout:\n{self.stdout}\n\nstderr:\n{self.stderr}"