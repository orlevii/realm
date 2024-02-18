import sys
from pathlib import Path

import pytest
from realm.utils.child_process import ChildProcess
from tests.common import IS_WINDOWS
from tests.test_services.pypiserver import PypiServer


@pytest.fixture(scope="module")
def pypi_server():
    with PypiServer() as pypi:
        yield pypi.get_url()


def _create_venv(clean_repo) -> Path:
    """
    :param clean_repo:
    :return: Python executable path
    """
    clean_repo_path = Path(clean_repo)
    venv_path = clean_repo_path.joinpath("venv")
    ChildProcess.run(f"{sys.executable} -m venv venv", cwd=clean_repo)
    if IS_WINDOWS:
        return venv_path.joinpath("Scripts").joinpath("python")
    return venv_path.joinpath("bin").joinpath("python")


def test_simple_publish(clean_repo, pypi_server):
    ChildProcess.run(
        f'realm run --scope pkg -- poetry config repositories.pypi-local "{pypi_server}" --local',
        cwd=clean_repo,
    )
    ChildProcess.run("realm build --scope pkg", cwd=clean_repo)
    ChildProcess.run(
        "realm run --scope pkg -- poetry publish -r pypi-local -u admin -p admin",
        cwd=clean_repo,
    )

    python_path = _create_venv(clean_repo)
    pip = f"{python_path} -m pip"
    ChildProcess.run(f"{pip} install pkg --index-url {pypi_server}", cwd=clean_repo)
    res = ChildProcess.run(f"{pip} freeze", cwd=clean_repo)
    assert "pkg==0.1.0" in res
