import os

import pytest
from pytest_mock import MockFixture
from realm.cli.application import Application
from realm.cli.commands.install import InstallCommand
from realm.cli.commands.ls import LsCommand
from realm.entities import Config, RealmContext
from realm.utils.child_process import ChildProcess

from tests.common import captured_output, get_tests_root_dir

REPO_DIR = get_tests_root_dir().joinpath("fixtures/test_workspace")


@pytest.fixture(scope="module")
def config():
    return Config.from_file(realm_json_file=str(REPO_DIR.joinpath("realm.json")))


@pytest.fixture
def realm_context(config):
    return RealmContext(config=config, projects=Application.get_projects(config))


def test_scan(realm_context):
    found = len(realm_context.projects)
    assert found == 2


@pytest.mark.parametrize("options", [{"paths": False}, {"paths": True}])
def test_ls(realm_context, options: dict):
    cmd = LsCommand(realm_context, **options)
    with captured_output() as (out, _):
        cmd.run()
    output = out.getvalue().strip()
    if options["paths"]:
        assert os.path.join("packages", "pkg_with_groups") in output
    else:
        assert "pkg@0.1.0" in output
        assert "pkg_with_groups@0.1.0" in output


def test_task_install(realm_context, mocker: MockFixture):
    install_cmd = InstallCommand(realm_context)
    run_patch = mocker.patch.object(ChildProcess, "run")
    install_cmd.run()

    for call_args in run_patch.call_args_list:
        assert call_args[0][0].startswith("poetry install")
    assert run_patch.call_count == 2


@pytest.mark.parametrize(
    "git_diff",
    [
        {"diff": "", "expected": ""},
        {"diff": "README.md", "expected": ""},
        {"diff": "packages/pkg/file", "expected": "pkg@0.1.0"},
        {"diff": "packages/pkg_with_groups/file", "expected": "pkg_with_groups@0.1.0"},
    ],
)
def test_git_diff(realm_context, git_diff: dict, mocker: MockFixture):
    def my_side_effect(*args, **kwargs):
        cmd = args[0]
        if cmd.startswith("git diff"):
            return git_diff["diff"]
        else:
            return realm_context.config.root_dir

    run_patch = mocker.patch.object(ChildProcess, "run")
    run_patch.side_effect = my_side_effect
    cmd = LsCommand(realm_context, since="main")

    with captured_output() as (out, _):
        cmd.run()
    output = out.getvalue().strip()
    assert output == git_diff["expected"]


@pytest.mark.parametrize(
    "filters",
    [
        {"scope": ["p*"], "expected": ["pkg@0.1.0", "pkg_with_groups@0.1.0"]},
        {"scope": ["p*"], "ignore": ["*with*"], "expected": ["pkg@0.1.0"]},
        {"scope": ["w*"], "expected": []},
    ],
)
def test_glob_star_filters(realm_context, filters: dict):
    cmd = LsCommand(
        realm_context, scope=filters.get("scope"), ignore=filters.get("ignore")
    )
    with captured_output() as (out, _):
        cmd.run()
    output = out.getvalue().strip()
    assert set(output.split()) == set(filters["expected"])


def test_match_filter(realm_context):
    cmd = LsCommand(realm_context, match=["labels.type=package"])
    with captured_output() as (out, _):
        cmd.run()
    output = out.getvalue().strip()
    assert output == "pkg@0.1.0"
