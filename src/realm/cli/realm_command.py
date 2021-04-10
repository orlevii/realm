import os
from abc import ABC
from concurrent.futures import ThreadPoolExecutor

from realm.entities import RealmContext

from .core.base_command import BaseCommand, T
from .realm_click_types import RealmClickCommand
from ..utils.filters.ignore import IgnoreFilter
from ..utils.filters.match import MatchFilter
from ..utils.filters.scope import ScopeFilter
from ..utils.filters.since import SinceFilter


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
        SinceFilter.apply(ctx=self.ctx,
                          since=self._params.get('since'))

        include_all_when_empty = self._params.get('all')
        if include_all_when_empty:
            if not any(self.ctx.projects):
                self.ctx.projects = self.ctx.all_projects

        ScopeFilter.apply(ctx=self.ctx,
                          scopes=self._params.get('scope'))

        IgnoreFilter.apply(ctx=self.ctx,
                           ignores=self._params.get('ignore'))

        MatchFilter.apply(ctx=self.ctx,
                          matches=self._params.get('match'))
