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

CONFIG_FILE = 'realm.json'


class Application:
    @classmethod
    def create(cls):
        grp = RealmClickGroup(callback=cls.init_context,
                              params=cls.global_options())

        grp.add_command(InitCommand)
        grp.add_command(LsCommand)
        grp.add_command(RunCommand)
        grp.add_command(InstallCommand)
        grp.add_command(TaskCommand)

        return grp

    @classmethod
    def global_options(cls):
        return [
            GlobalOption(['--version', '-V'],
                         is_flag=True,
                         callback=cls.print_version,
                         help='Display realm version'),
            GlobalOption(['--parallelism', '-p'],
                         type=click.INT,
                         show_default=True,
                         default=1,
                         help='Sets the parallelism for the command (if supported)'),
            GlobalOption(['--since'],
                         help='Includes only projects changed since the specified ref'),
            GlobalOption(['--all'],
                         is_flag=True,
                         help='Include all projects if no projects were changed when using the --since filter'),
            GlobalOption(['--scope'],
                         type=click.STRING,
                         help='Includes only projects that match the given pattern'),
            GlobalOption(['--ignore'],
                         type=click.STRING,
                         help='Filters out projects that match the given pattern'),
            GlobalOption(['--match'],
                         type=click.STRING,
                         help='Filters by a field specified in `pyproject.toml`')
        ]

    @staticmethod
    def print_version(ctx, value):
        if value:
            msg = 'Realm {}'.format(click.style(__version__, fg='yellow'))
            click.echo(msg)

            sys.exit(0)

    @staticmethod
    @click.pass_context
    def init_context(ctx, **kwargs):
        cfg = Application.read_config()
        projects = Application.get_projects(cfg)
        ctx.obj = RealmContext(config=cfg,
                               projects=projects)

    @classmethod
    def read_config(cls):
        current = pathlib.Path(os.getcwd())
        current = current.joinpath(CONFIG_FILE)
        possible_paths = [x.joinpath(CONFIG_FILE) for x in current.parents]
        for p in possible_paths:
            if p.exists():
                with p.open() as f:
                    cfg_json = json.load(f)
                    return Config(root_dir=str(p.parent),
                                  **cfg_json)

        return Config()

    @classmethod
    def get_projects(cls, cfg: Config) -> List[Project]:
        tmp_candidates = [glob.glob(os.path.join(cfg.root_dir, p)) for p in cfg.projects]
        candidates = []
        for lst in tmp_candidates:
            for c in lst:
                candidates.append(os.path.abspath(c))

        projects = []
        for path in candidates:
            if 'pyproject.toml' in os.listdir(path):
                projects.append(Project(source_dir=path,
                                        root_dir=cfg.root_dir))

        return projects


cli = Application.create()
