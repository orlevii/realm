from tempfile import TemporaryDirectory

from realm.utils.child_process import ChildProcess


def test_init_command():
    with TemporaryDirectory("_realm") as tmp_dir:
        ChildProcess.run("realm init", cwd=tmp_dir).strip()
        output = ChildProcess.run("realm ls", cwd=tmp_dir).strip()
        assert output == "pgk@0.1.0"
