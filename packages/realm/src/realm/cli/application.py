import glob
import json
import os
import pathlib
import sys
from typing import List

import click

from realm.entities import Config, Project, RealmContext
from realm.version import __version__

from .commands.init import InitCommand
from .commands.install import InstallCommand
from .commands.ls import LsCommand
from .commands.run import RunCommand
from .commands.task import TaskCommand
from .core.params import GlobalOption
from .realm_click_types import RealmClickGroup




class Application:
    @classmethod
    def create(cls):
        grp = RealmClickGroup(params=cls.global_options())

        grp.add_command(InitCommand)
        grp.add_command(LsCommand)
        grp.add_command(RunCommand)
        grp.add_command(InstallCommand)
        grp.add_command(TaskCommand)

        return grp

    @classmethod
    def global_options(cls):
        return [
            GlobalOption(
                ["--version", "-V"],
                is_flag=True,
                callback=cls.print_version,
                help="Display realm version",
            ),
            GlobalOption(
                ["--parallelism", "-p"],
                type=click.INT,
                show_default=True,
                default=1,
                help="Sets the parallelism for the command (if supported)",
            ),
            GlobalOption(
                ["--since"],
                help="Includes only projects changed since the specified ref",
            ),
            GlobalOption(
                ["--all"],
                is_flag=True,
                help="Include all projects if no projects were changed when using the --since filter",
            ),
            GlobalOption(
                ["--scope"],
                type=click.STRING,
                help="Includes only projects that match the given pattern",
                multiple=True,
            ),
            GlobalOption(
                ["--ignore"],
                type=click.STRING,
                help="Filters out projects that match the given pattern",
                multiple=True,
            ),
            GlobalOption(
                ["--match"],
                type=click.STRING,
                help="Filters by a field specified in `pyproject.toml`",
                multiple=True,
            ),
        ]

    @staticmethod
    def print_version(ctx, _, value):
        if value:
            msg = "Realm {}".format(click.style(__version__, fg="yellow"))
            click.echo(msg)

            sys.exit(0)


cli = Application.create()
