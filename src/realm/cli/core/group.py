from typing import Type

import click

from .base_command import BaseCommand


class Group(click.Group):
    def add_command(self, cmd: Type[BaseCommand], name=None):
        created_cmd = cmd.to_command()
        if not created_cmd.params:
            created_cmd.params = []
        created_cmd.params.extend(self.params)
        super().add_command(created_cmd,
                            name=name)

    def add_group(self, grp: click.Group, name=None):
        if not grp.params:
            grp.params = []
        grp.params.extend(self.params)
        # Call the original add_command that also handles group
        super(Group, self).add_command(grp,
                                       name=name)
