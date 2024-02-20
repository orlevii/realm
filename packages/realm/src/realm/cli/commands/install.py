import sys

import click

from realm.cli.realm_command import RealmCommand
from realm.entities.project import Project


class InstallCommand(RealmCommand[dict]):
    NAME = "install"
    HELP_MESSAGE = """
    Executes "poetry install" on all projects
    """

    def run(self):
        self._run_in_pool(self._install)

    @staticmethod
    def _install(project: Project):
        try:
            out = project.execute_cmd("poetry install")
            if out:
                # used only for tests :(
                click.echo(out)
        except Exception as e:
            click.echo(e, err=True)
            sys.exit(1)
