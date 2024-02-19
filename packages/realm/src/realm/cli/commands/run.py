import shlex
import sys
from functools import cached_property

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
        self.logger.debug(f"Running command: {self.full_cmd}")
        try:
            self._run_in_pool(self._run_cmd)
        except Exception as e:
            click.echo(e, err=True)
            sys.exit(1)

    @cached_property
    def full_cmd(self):
        cmd = self.params.get("command")
        full_cmd = shlex.join(cmd)
        return full_cmd

    def _run_cmd(self, project: Project):
        try:
            out = project.execute_cmd(self.full_cmd)
            if out:
                # used only for tests :(
                click.echo(out)
        except Exception as e:
            click.echo(e, err=True)
            sys.exit(1)
