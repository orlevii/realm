from functools import partial
from pathlib import Path

from realm.utils.child_process import ChildProcess

fixtures_path = Path(__file__).parent.parent.joinpath("fixtures")

PACKAGES_REPO = "packages_repo"


def create_run_in_fixture_fn(fixutre_relative_path: str):
    cwd = str(fixtures_path.joinpath(fixutre_relative_path))
    return partial(ChildProcess.run, cwd=cwd)


run_in_root = create_run_in_fixture_fn("..")
