import multiprocessing as mp
from abc import ABC

from realm.entities import RealmContext

from .base import BaseCommand, T
from ..utils.filters import apply_since_filters


class RealmCommand(BaseCommand[T], ABC):
    def __init__(self, ctx: RealmContext, **kwargs):
        super().__init__(ctx, **kwargs)
        # Just for the type annotation
        self.ctx = ctx

        self.pool = mp.Pool(self._params['parallelism'])
        self.__filter_projects()

    def __filter_projects(self):
        since = self._params.get('since')
        include_all_when_empty = True
        if since:
            apply_since_filters(self.ctx, since, include_all_when_empty)
