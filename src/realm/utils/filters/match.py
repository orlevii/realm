import fnmatch
from typing import List

from realm.entities import RealmContext, Project


class MatchFilter:
    @classmethod
    def apply(cls, ctx: RealmContext, matches: List[str]):
        if not matches:
            return

        filtered = []
        for match in matches:
            field, _, value = match.partition('=')
            f1 = f'tool.realm.{field}'
            f2 = f'tool.{field}'
            f = {p for p
                 in ctx.projects
                 if cls._matches(p, f1, value) or
                 cls._matches(p, f2, value)}
            filtered.append(f)

        ctx.projects = cls._union(filtered)

    @classmethod
    def _matches(cls, project: Project, field: str, pattern: str) -> bool:
        value = project.extract_field(field)
        if not value:
            return False
        return fnmatch.fnmatch(value, pattern)

    @classmethod
    def _union(cls, filtered):
        result = filtered[0]
        for f in filtered:
            result = result.union(f)
        return list(result)
