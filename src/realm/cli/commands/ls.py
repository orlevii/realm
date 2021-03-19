import click
from realm.cli.realm_command import RealmCommand


class LsCommand(RealmCommand[dict]):
    NAME = 'ls'
    PARAMS = [
        click.Option(['--paths'], is_flag=True)
    ]

    def run(self):
        for p in self.ctx.projects:
            if self.params.get('paths'):
                click.echo(f'{p.relative_path}')
            else:
                click.echo(f'{p.name}@{p.version}')
