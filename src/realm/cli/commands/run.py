import click
from realm.cli.realm_command import RealmCommand
from realm.utils import await_all


class RunCommand(RealmCommand[dict]):
    NAME = 'run'
    HELP_MESSAGE = """
    Executes a command on all projects
    """
    PARAMS = [
        click.Argument(['command'], type=click.STRING, nargs=-1)
    ]

    def run(self):
        cmd = self.params.get('command')
        full_cmd = ' '.join(cmd)
        futures = [self.pool.submit(project.execute_cmd, full_cmd)
                   for project
                   in self.ctx.projects]

        await_all(futures)
