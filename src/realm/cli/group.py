from typing import Type

import click

from .base import BaseCommand


class Group(click.Group):
    def add_command(self, cmd: Type[BaseCommand], name=None):
        if not cmd.PARAMS:
            cmd.PARAMS = []
        cmd.PARAMS.extend(self.params)
        super().add_command(cmd.to_command(),
                            name=name)

    def add_group(self, grp: click.Group, name=None):
        if not grp.params:
            grp.params = []
        grp.params.extend(self.params)
        # Call the original add_command that also handles group
        super(Group, self).add_command(grp,
                                       name=name)
