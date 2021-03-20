import shlex

import subprocess


class ChildProcess:

    @staticmethod
    def run(command, **kwargs) -> str:
        params = dict(stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE)
        params.update(kwargs)
        if not kwargs.get('shell'):
            command = shlex.split(command)
        p = subprocess.Popen(command,
                             **params)
        out, err = p.communicate()
        if p.returncode != 0:
            raise RuntimeError(f'Failed running command: {command}, stdout: {out}, stderr: {err}')

        if out:
            if isinstance(out, bytes):
                out = out.decode()

        return out
