import fnmatch
from typing import List

from realm.entities import RealmContext


class ScopeFilter:
    @classmethod
    def apply(cls, ctx: RealmContext, scopes: List[str]):
        if not scopes:
            return

        filtered = []
        for scope in scopes:
            f = {p for p in ctx.projects if fnmatch.fnmatch(p.name, scope)}
            filtered.append(f)

        ctx.projects = cls._union(filtered)

    @classmethod
    def _union(cls, filtered):
        result = filtered[0]
        for f in filtered:
            result = result.union(f)
        return list(result)
