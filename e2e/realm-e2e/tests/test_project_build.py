import pytest
from realm.utils.child_process import ChildProcess
from tests.containers.pypiserver import PypiServer


@pytest.fixture(scope="module")
def pypi_server():
    with PypiServer() as pypi:
        yield pypi.get_url()


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
