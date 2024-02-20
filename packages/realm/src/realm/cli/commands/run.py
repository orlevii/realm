import shlex
import sys

import click

from realm.cli.realm_command import RealmCommand
from realm.entities import Project


class RunCommand(RealmCommand[dict]):
    NAME = "run"
    HELP_MESSAGE = """
    Executes a command on all projects
    """
    PARAMS = [click.Argument(["command"], type=click.STRING, nargs=-1)]

    def run(self):
        full_cmd = self.get_full_cmd()
        self.logger.debug(f"Running command: {full_cmd}")
        try:
            self._run_in_pool(self._run_cmd, cmd=full_cmd)
        except Exception as e:
            click.echo(e, err=True)
            sys.exit(1)

    def get_full_cmd(self):
        cmd = self.params.get("command")
        full_cmd = shlex.join(cmd)
        return full_cmd

    @staticmethod
    def _run_cmd(project: Project, cmd: str):
        try:
            out = project.execute_cmd(cmd)
            if out:
                # used only for tests :(
                click.echo(out)
        except Exception as e:
            click.echo(e, err=True)
            sys.exit(1)
