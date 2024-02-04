import fnmatch
from typing import List

from realm.entities import RealmContext


class IgnoreFilter:
    @classmethod
    def apply(cls, ctx: RealmContext, ignores: List[str]):
        if not ignores:
            return

        filtered = []
        for ignore in ignores:
            f = {p for p in ctx.projects if not fnmatch.fnmatch(p.name, ignore)}
            filtered.append(f)

        ctx.projects = cls._intersect(filtered)

    @classmethod
    def _intersect(cls, filtered):
        result = filtered[0]
        for f in filtered:
            result = result.intersection(f)
        return list(result)
