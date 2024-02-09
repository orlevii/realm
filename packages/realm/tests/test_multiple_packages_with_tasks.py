import os
import pytest
from pytest_mock import MockFixture
from realm.cli.application import Application
from realm.cli.commands.install import InstallCommand
from realm.cli.commands.ls import LsCommand
from realm.cli.commands.task import TaskCommand
from realm.entities import Config, RealmContext
from realm.utils.child_process import ChildProcess

from tests.common import captured_output, get_tests_root_dir

REPO_DIR = get_tests_root_dir().joinpath("fixtures/multiple_packages_with_tasks")



@pytest.fixture(scope="class")
def config():
    return Config.from_file(realm_json_file=str(REPO_DIR.joinpath("realm.json")))


@pytest.fixture
def realm_context(config):
    return RealmContext(config=config, projects=Application.get_projects(config))


def test_scan(realm_context):
    found = len(realm_context.projects)
    assert found == 2

@pytest.mark.parametrize("options", [{"paths": False},{"paths": True}])
def test_ls(realm_context, options: dict):
    cmd = LsCommand(realm_context, **options)
    with captured_output() as (out, _):
        cmd.run()
    output = out.getvalue().strip()
    if options["paths"]:
        assert os.path.join("packages", "pkg_with_groups")in output
    else:
        assert "pkg@0.1.0" in output
        assert "pkg_with_groups@0.1.0" in output


def test_task_install(realm_context, mocker: MockFixture):
    
    install_cmd = InstallCommand(realm_context)
    run_patch = mocker.patch.object(ChildProcess, "run")
    install_cmd.run()

    for call_args in run_patch.call_args_list:
        assert call_args[0][0].startswith("poetry install")

# def test_task_install(realm_context):
#     install_cmd = InstallCommand(realm_context)
#     task_cmd = TaskCommand(realm_context, task_name="test")

#     assert len(task_cmd.ctx.projects) == 1

#     with captured_output(stderr=False) as (out, _):
#         install_cmd.run()
#         task_cmd.run()

#     output = out.getvalue()
#     assert "Installing the current project: pkg" in output
#     assert 'Poe => python -m unittest discover -s tests -v -p "test_*.py"' in output


# def test_git_diff(realm_context):
#     cmd = LsCommand(realm_context, since=".")
#     with captured_output() as (out, _):
#         cmd.run()
#     output = out.getvalue().strip()
#     assert output == ""


# def test_git_diff_with_change(realm_context):
#     pkg_proj = next(p for p in realm_context.projects if p.name == "pkg")
#     try:
#         with pkg_proj.source_dir.joinpath("pyproject.toml").open("a") as f:
#             print("", file=f)

#         cmd = LsCommand(realm_context, since=".")

#         with captured_output() as (out, _):
#             cmd.run()
#         output = out.getvalue().strip()
#         assert output == "pkg@0.1.0"
#     finally:
#         ChildProcess.run(f"git checkout {pkg_proj.source_dir}")


# def test_scope_filter(realm_context):
#     cmd = LsCommand(realm_context, scope=["p*"], ignore=["*with*"])
#     with captured_output() as (out, _):
#         cmd.run()
#     output = out.getvalue().strip()
#     assert output == "pkg@0.1.0"


# def test_ignore_filter(realm_context):
#     cmd = LsCommand(realm_context, ignore=["p*"])
#     with captured_output() as (out, _):
#         cmd.run()
#     output = out.getvalue().strip()
#     assert output == ""


# def test_match_filter(realm_context):
#     cmd = LsCommand(realm_context, match=["labels.type=package"])
#     with captured_output() as (out, _):
#         cmd.run()
#     output = out.getvalue().strip()
#     assert output == "pkg@0.1.0"
