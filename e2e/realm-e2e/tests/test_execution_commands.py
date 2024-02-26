import json

from realm.utils.child_process import ChildProcess


def test_install_command(clean_repo):
    ChildProcess.run(
        "poetry config virtualenvs.in-project true --local", cwd=clean_repo
    )
    output = ChildProcess.run("realm install", cwd=clean_repo).strip()

    assert "Installing dependencies from lock file" in output, output


def test_task_command(clean_repo):
    output = ChildProcess.run("realm task test", cwd=clean_repo).strip()
    assert "Running task test for: pkg" in output
    assert 'Poe => python -m unittest discover -s tests -v -p "test_*.py"' in output
    assert "Running task test for: pkg_with_groups" not in output


def test_run_command(clean_repo):
    num_projects = len(ChildProcess.run("realm ls", cwd=clean_repo).strip().split())
    output = ChildProcess.run("realm run echo hello", cwd=clean_repo).strip().split()
    assert output == ["hello"] * num_projects


def test_run_command_2(clean_repo):
    ChildProcess.run(
        "realm -vvv run -- echo hello > file", cwd=clean_repo
    ).strip().split()


def test_run_command_3(clean_repo):
    out = ChildProcess.run(
        "realm run --scope pkg -- python script.py 'arg with space'", cwd=clean_repo
    ).strip()
    parsed_out = json.loads(out)
    assert parsed_out == ["script.py", "arg with space"]
