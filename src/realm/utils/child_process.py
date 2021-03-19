import shlex

import subprocess


class ChildProcess:

    @staticmethod
    def run(command) -> str:
        p = subprocess.Popen(shlex.split(command),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            raise RuntimeError(f'Failed running command: {command}, stdout: {out}, stderr: {err}')

        if out:
            out = out.decode()

        return out
