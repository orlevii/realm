import fnmatch
from concurrent.futures import ThreadPoolExecutor, Executor
import os
from abc import ABC

from realm.entities import RealmContext

from .core.base_command import BaseCommand, T
from .realm_click_types import RealmClickCommand
from ..utils.filters import apply_since_filters


class RealmCommand(BaseCommand[T], ABC):
    CLICK_COMMAND_CLS = RealmClickCommand

    def __init__(self, ctx: RealmContext, **kwargs):
        super().__init__(ctx, **kwargs)
        # Just for the type annotation
        self.ctx = ctx
        self.pool = ThreadPoolExecutor(self._params.get('parallelism', 1))
        self._filter_projects()
        os.environ['REALM_ROOT_PATH'] = self.ctx.config.root_dir

    def _filter_projects(self):
        # TODO: refactor into smaller methods, allow multiple values
        since = self._params.get('since')
        include_all_when_empty = self._params.get('all')
        if since:
            apply_since_filters(self.ctx, since)
            if include_all_when_empty:
                if not any(self.ctx.projects):
                    self.ctx.projects = self.ctx.all_projects

        scope = self._params.get('scope')
        if scope:
            self.ctx.projects = [p for p
                                 in self.ctx.projects
                                 if fnmatch.fnmatch(p.name, scope)]

        ignore = self._params.get('ignore')
        if ignore:
            self.ctx.projects = [p for p
                                 in self.ctx.projects
                                 if not fnmatch.fnmatch(p.name, scope)]

        match = self._params.get('match')
        if match:
            field, _, value = match.partition('=')
            f1 = f'tool.realm.{field}'
            f2 = f'tool.{field}'
            self.ctx.projects = [p for p
                                 in self.ctx.projects
                                 if str(p.extract_field(f1)) == value or
                                 str(p.extract_field(f2)) == value]
