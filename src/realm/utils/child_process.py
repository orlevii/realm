import shlex

import subprocess


class ChildProcess:
    FORCE_CAPTURE = False
    CAPTURE_PARAMS = dict(stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    @classmethod
    def run(cls, command, **kwargs) -> str:
        params = dict(cls.CAPTURE_PARAMS)
        params.update(kwargs)

        if cls.FORCE_CAPTURE:
            params.update(cls.CAPTURE_PARAMS)

        if not kwargs.get('shell'):
            command = shlex.split(command)
        p = subprocess.Popen(command,
                             **params)
        out, err = p.communicate()
        if out and isinstance(out, bytes):
            out = out.decode()

        if err and isinstance(err, bytes):
            err = err.decode()

        if p.returncode != 0:
            raise RuntimeError(f'Failed running command: {command};\nstdout: {out};\nstderr: {err};')

        return out
