import pytest
from realm.utils.child_process import ChildProcess
from realm.version import __version__


@pytest.fixture(scope="class")
def init_child_process():
    ChildProcess.FORCE_CAPTURE = True


def test_version():
    out = ChildProcess.run("realm -V").strip()
    assert out == f"Realm {__version__}"
