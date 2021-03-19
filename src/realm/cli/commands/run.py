import click
from realm.cli.realm_command import RealmCommand


class RunCommand(RealmCommand[dict]):
    NAME = 'run'
    PARAMS = [
        click.Argument(['command'], type=click.STRING)
    ]

    def run(self):
        for project in self.ctx.projects:
            project.execute_cmd(self.params.get('command'))
