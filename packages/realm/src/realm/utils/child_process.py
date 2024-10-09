from __future__ import annotations

import shlex
import subprocess


class ChildProcess:
    FORCE_CAPTURE = False
    CAPTURE_PARAMS = {"stdout": subprocess.PIPE}

    @classmethod
    def run(cls, command: str | list[str], **kwargs) -> str:
        params = dict(cls.CAPTURE_PARAMS)
        params.update(kwargs)

        if cls.FORCE_CAPTURE:
            params.update(cls.CAPTURE_PARAMS)

        if isinstance(command, str) and not kwargs.get("shell"):
            command = shlex.split(command, posix=False)
        p = subprocess.Popen(command, **params)
        out, err = p.communicate()
        if isinstance(out, bytes):
            out = out.decode("utf-8", "ignore")

        if isinstance(err, bytes):
            err = err.decode("utf-8", "ignore")

        if p.returncode != 0:
            raise RuntimeError(
                f"Failed running command: {command};\nstdout: {out};\nstderr: {err};"
            )

        return out
