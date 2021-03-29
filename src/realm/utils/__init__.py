from concurrent.futures import Future
from typing import Iterable


def await_all(futures: Iterable[Future], timeout=None):
    return [f.result(timeout) for f in futures]
