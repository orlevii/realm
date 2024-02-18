import shutil
from tempfile import TemporaryDirectory

import pytest
from realm.utils.child_process import ChildProcess
from tests.common import PACKAGES_REPO_PATH


@pytest.fixture(scope="session")
def temp_repo():
    ChildProcess.FORCE_CAPTURE = True
    with TemporaryDirectory("_realm") as tmp_dir:
        ChildProcess.run("git init --initial-branch main", cwd=tmp_dir)
        ChildProcess.run("git config user.email test@realm.com", cwd=tmp_dir)
        ChildProcess.run("git config user.name Test", cwd=tmp_dir)
        shutil.copytree(str(PACKAGES_REPO_PATH), tmp_dir, dirs_exist_ok=True)
        ChildProcess.run("git add .", cwd=tmp_dir)
        ChildProcess.run("git commit -am 'first commit'", cwd=tmp_dir)
        ChildProcess.run("git checkout -b bak", cwd=tmp_dir)
        ChildProcess.run("git checkout main", cwd=tmp_dir)
        yield tmp_dir


@pytest.fixture()
def clean_repo(temp_repo: str):
    yield temp_repo
    ChildProcess.run("git reset --hard bak", cwd=temp_repo)
    ChildProcess.run("git checkout main", cwd=temp_repo)
    ChildProcess.run("git reset --hard bak", cwd=temp_repo)
    ChildProcess.run("git clean -dfx", cwd=temp_repo)
