[![Build Status](https://travis-ci.org/wtsi-hgi/python-git-subrepo.svg?branch=master)](https://travis-ci.org/wtsi-hgi/python-git-subrepo)
[![codecov](https://codecov.io/gh/wtsi-hgi/python-git-subrepo/branch/master/graph/badge.svg)](https://codecov.io/gh/wtsi-hgi/python-git-subrepo)
[![PyPI version](https://badge.fury.io/py/gitsubrepo.svg)](https://badge.fury.io/py/gitsubrepo)

# Git Subrepo Python Wrapper
In the same way that [`GitPython`](https://pypi.python.org/pypi/GitPython/) wraps `git`, this library provides easy 
access to [git subrepo](https://github.com/ingydotnet/git-subrepo) in Python.


## How to use
### Prerequisites
 - git >= 2.10.0 (on path)
 - git-subrepo >= 0.3.1
 - python >= 3.6


### Installation
Stable releases can be installed via [PyPI](https://pypi.python.org/pypi/gitsubrepo):
```bash
$ pip install gitsubrepo
```

Bleeding edge versions can be installed directly from GitHub:
```bash
$ pip install git+https://github.com/wtsi-hgi/python-git-subrepo.git@${commitIdBranchOrTag}#egg=gitsubrepo
```

To declare this library as a dependency of your project, add it to your `requirement.txt` file.


### API
The library currently supports 3 `git subrepo` operations: `clone`, `pull` and `status`. Please see the documentation 
for specific information on how to use these methods.

Example usage:
```python
import gitsubrepo

remote_repository = "https://github.com/colin-nolan/test-repository.git"
repository_location = "/tmp/repo"
subrepo_location = f"{repository_location}/subrepo"
branch = "develop"

commit_reference = gitsubrepo.clone(remote_repository, subrepo_location, branch=branch)
updated_commit_reference = gitsubrepo.pull(subrepo_location)

subrepo_remote, subrepo_branch, subrepo_commit = gitsubrepo.status(subrepo_location)
assert subrepo_remote == remote_repository
assert subrepo_branch == branch
```


## Development
### Setup
Install both library dependencies and the dependencies needed for testing:
```bash
$ pip install -q -r requirements.txt
$ pip install -q -r test_requirements.txt
```

### Testing
To run the tests and generate a coverage report with unittest:
```bash
./test-runner.sh
```
If you wish to run the tests inside a Docker container, build `Docker.test`.


## License
[MIT license](LICENSE.txt).

Copyright (c) 2017 Genome Research Limited
