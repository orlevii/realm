from pathlib import Path

import pytest
from realm.utils.child_process import ChildProcess
from tests.common import temp_git_branch


def test_verify_project(clean_repo):
    output = ChildProcess.run("realm ls", cwd=clean_repo).strip().split()
    assert len(output) > 0


def test_since_empty(clean_repo):
    output = ChildProcess.run("realm ls --since main", cwd=clean_repo).strip()
    assert output == ""


def test_since_empty_all_flag(clean_repo):
    cmd = "realm ls --since main --all"
    output = ChildProcess.run(cmd, cwd=clean_repo).strip().split()

    all_cmd = "realm ls"
    expected = ChildProcess.run(all_cmd, cwd=clean_repo).strip().split()
    assert set(output) == set(expected)


@pytest.mark.parametrize("package_name", ["pkg", "pkg_with_groups"])
def test_changed_file(clean_repo, package_name: str):
    with temp_git_branch(repo_path=clean_repo, branch_name="test1"):
        file = (
            Path(clean_repo)
            .joinpath("packages")
            .joinpath(package_name)
            .joinpath("pyproject.toml")
        )
        with file.open("a") as f:
            f.write("\n")
        ChildProcess.run("git commit -am 'change'", cwd=clean_repo)
        output = ChildProcess.run("realm ls --since main", cwd=clean_repo).strip()
        assert output == f"{package_name}@0.1.0"


@pytest.mark.parametrize(
    "changes",
    [
        {"package_name": "dep_a", "expected": {"dep_a@0.1.0"}},
        {"package_name": "dep_b", "expected": {"dep_a@0.1.0", "dep_b@0.2.0"}},
        {
            "package_name": "dep_c",
            "expected": {"dep_a@0.1.0", "dep_b@0.2.0", "dep_c@0.3.0"},
        },
    ],
)
def test_changed_file_affected(clean_repo, changes: dict):
    package_name = changes["package_name"]
    expected = changes["expected"]
    with temp_git_branch(repo_path=clean_repo, branch_name="test2"):
        file = (
            Path(clean_repo)
            .joinpath("packages")
            .joinpath(package_name)
            .joinpath("pyproject.toml")
        )
        with file.open("a") as f:
            f.write("\n")
        ChildProcess.run("git commit -am 'change'", cwd=clean_repo)
        output = set(
            ChildProcess.run("realm -vvv ls --since main", cwd=clean_repo)
            .strip()
            .split()
        )
        assert output == expected
