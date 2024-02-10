from contextlib import contextmanager
from functools import partial
from pathlib import Path

from realm.utils.child_process import ChildProcess

fixtures_path = Path(__file__).parent.parent.joinpath("fixtures")

PACKAGES_REPO = "packages_repo"
PACKAGES_REPO_PATH = fixtures_path.joinpath(PACKAGES_REPO)


def create_run_in_fixture_fn(fixutre_relative_path: str):
    cwd = str(fixtures_path.joinpath(fixutre_relative_path))
    return partial(ChildProcess.run, cwd=cwd)


@contextmanager
def temp_git_branch(repo_path: str, branch_name: str):
    ChildProcess.run(f"git checkout -b {branch_name}", cwd=repo_path)
    try:
        yield
    finally:
        ChildProcess.run("git checkout main", cwd=repo_path)
        ChildProcess.run(f"git branch -D {branch_name}", cwd=repo_path)


run_in_root = create_run_in_fixture_fn("..")
