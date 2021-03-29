import click
from realm.cli.realm_command import RealmCommand
from realm.utils import await_all


class InstallCommand(RealmCommand[dict]):
    NAME = 'install'
    HELP_MESSAGE = """
    Executes "poetry install" on all projects
    """

    def run(self):
        futures = [self.pool.submit(self._install, project)
                   for project
                   in self.ctx.projects]

        await_all(futures)

    @staticmethod
    def _install(project):
        out = project.execute_cmd('poetry install')
        if out:
            # used only for tests :(
            click.echo(out)
