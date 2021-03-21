from typing import Type

import click
import click_help_colors as chc

from .base import BaseCommand


class Group(chc.HelpColorsMixin, click.Group):
    def add_command(self, cmd: Type[BaseCommand], name=None):
        created_cmd = cmd.to_command()
        if not created_cmd.params:
            created_cmd.params = []
        created_cmd.params.extend(self.params)
        created_cmd.help_headers_color = self.help_headers_color
        created_cmd.help_options_color = self.help_options_color
        super().add_command(created_cmd,
                            name=name)

    def add_group(self, grp: click.Group, name=None):
        if not grp.params:
            grp.params = []
        grp.params.extend(self.params)
        # Call the original add_command that also handles group
        super(Group, self).add_command(grp,
                                       name=name)
