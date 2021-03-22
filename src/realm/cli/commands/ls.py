import click
from realm.cli.realm_command import RealmCommand


class LsCommand(RealmCommand[dict]):
    NAME = 'ls'
    HELP_MESSAGE = """
    Prints all projects managed
    """
    PARAMS = [
        click.Option(['--paths'],
                     help='Prints relative paths of the projects',
                     is_flag=True)
    ]

    def run(self):
        for p in self.ctx.projects:
            if self.params.get('paths'):
                click.echo(f'{p.relative_path}')
            else:
                click.echo(f'{p.name}@{p.version}')
