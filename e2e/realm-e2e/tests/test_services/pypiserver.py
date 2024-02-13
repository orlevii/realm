import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from time import sleep


class PypiServer:
    def __init__(self, port: int = 8080):
        self.port = port
        self.tempfolder = Path().joinpath("pypiserver")
        self.htpasswd = self.tempfolder.joinpath(".htpasswd")
        self.cmd = [
            "pypi-server",
            "run",
            "-P",
            str(self.htpasswd),
            "-p",
            str(self.port),
            str(self.tempfolder),
        ]
        self.process: subprocess.Popen = None

    def __enter__(self):
        try:
            return self.start()
        except Exception as _:
            self.stop()
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        self.tempfolder.mkdir(parents=True, exist_ok=True)
        self.htpasswd.write_text("admin:admin")
        print(f'pypi_server_cmd={self.cmd}', file=sys.stderr)
        self.process = subprocess.Popen(self.cmd)
        self._connect()
        return self

    def _connect(self):
        retries = 10
        while True:
            retries -= 1
            try:
                res = urllib.request.urlopen(self.get_url())
                if res.status == 200:
                    return
                raise Exception()
            except Exception:
                if retries <= 0:
                    raise
                sleep(1)

    def get_url(self):
        return f"http://localhost:{self.port}"

    def stop(self):
        if self.process:
            self.process.terminate()
        if self.tempfolder.is_dir():
            shutil.rmtree(self.tempfolder)
