import pathlib
import sys
from contextlib import contextmanager
from io import StringIO

from realm.utils.child_process import ChildProcess


def get_tests_root_dir():
    return pathlib.Path(__file__).parent.absolute()


@contextmanager
def captured_output(stdout=True, stderr=True):
    """
    :param stdout: Capture stdout
    :param stderr: Capture stderr
    :return:
    """
    ChildProcess.FORCE_CAPTURE = True

    new_out = StringIO() if stdout else sys.stdout
    new_err = StringIO() if stderr else sys.stderr
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        ChildProcess.FORCE_CAPTURE = False
        sys.stdout, sys.stderr = old_out, old_err
