import click
from realm.cli.realm_command import RealmCommand


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
        for project in self.ctx.projects:
            project.execute_cmd(full_cmd)
