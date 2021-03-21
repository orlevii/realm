import click
from realm.cli.formatter import RealmFormatHelpMixin

from .core.group import Group


class RealmClickCommand(RealmFormatHelpMixin, click.Command):
    pass


class RealmClickGroup(RealmFormatHelpMixin, Group):
    pass
