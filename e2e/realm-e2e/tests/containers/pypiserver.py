import urllib.request

from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_container_is_ready


class PypiServer(DockerContainer):
    def __init__(self, port_to_expose: int = 8080):
        super().__init__(
            "pypiserver/pypiserver:v2.0.1",
            platform="linux/amd64",
            entrypoint=[
                "bash",
                "-c",
                "echo 'admin:admin' > .htpasswd && pypi-server -P .htpasswd packages -p 8080",
            ],
        )
        self.port_to_expose = port_to_expose
        self.with_exposed_ports(self.port_to_expose)
        self.with_command("run -P .htpasswd packages")

    def start(self):
        super().start()
        self._connect()
        return self

    @wait_container_is_ready()
    def _connect(self):
        res = urllib.request.urlopen(self.get_url())
        if res.status != 200:
            raise Exception()

    def get_url(self):
        host = self.get_container_host_ip()
        port = self.get_exposed_port(self.port_to_expose)
        return f"http://{host}:{port}"
