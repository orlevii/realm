from realm.version import __version__
from tests.common import run_in_root


def test_version():
    out = run_in_root("realm -V").strip()
    assert out == f"Realm {__version__}"
