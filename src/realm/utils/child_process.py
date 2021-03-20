import shlex

import subprocess


class ChildProcess:

    @staticmethod
    def run(command, **kwargs) -> str:
        p = subprocess.Popen(shlex.split(command),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             **kwargs)
        out, err = p.communicate()
        if p.returncode != 0:
            raise RuntimeError(f'Failed running command: {command}, stdout: {out}, stderr: {err}')

        if out:
            if isinstance(out, bytes):
                out = out.decode()

        return out
