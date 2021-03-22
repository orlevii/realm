import click
from realm.cli.formatter import RealmFormatHelpMixin

from .core.group import Group


class RealmClickCommand(RealmFormatHelpMixin, click.Command):
    pass


class RealmClickGroup(RealmFormatHelpMixin, Group):
    def format_options(self, ctx, formatter):
        RealmFormatHelpMixin.format_options(self, ctx, formatter)
        self.format_commands(ctx, formatter)
