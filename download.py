import pathlib
import shutil

import git

VERSION = "3.65.0"
URL = "https://github.com/treeverse/dvc"

path = pathlib.Path(__file__).parent.absolute()
dvc = path / "dvc"

try:
    shutil.rmtree(dvc)
except FileNotFoundError:
    pass

# NOTE: need full git clone for version detection
# by setuptools-scm
repo = git.Repo.clone_from(URL, dvc)
repo.git.checkout(VERSION)
