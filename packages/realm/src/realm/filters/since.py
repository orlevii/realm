import os
from typing import List

from realm.entities import RealmContext
from realm.utils.child_process import ChildProcess


class SinceFilter:
    @classmethod
    def apply(cls, ctx: RealmContext, since):
        if not since:
            return

        changed_projects = cls.get_changed_projects(ctx, since)
        affected = set(changed_projects)
        prev_len = 0
        new_len = len(affected)
        while prev_len != new_len:
            prev_len = new_len
            affected_cpy = set(affected)
            for p in affected:
                p_dependent = ctx.dependency_graph.projects_affected[p]
                affected_cpy = affected_cpy.union(p_dependent)
            affected = affected_cpy
            new_len = len(affected)

        ctx.projects = affected

    @classmethod
    def get_changed_projects(cls, ctx: RealmContext, since):
        changed_files = ChildProcess.run(f"git diff --name-only {since}")
        git_root = ChildProcess.run("git rev-parse --show-toplevel")
        git_root = git_root.strip() if git_root else ""

        relative_realm_repo_path = ctx.config.root_dir[len(git_root) :].lstrip(os.sep)

        changed_files = cls.parse_changed_files(changed_files)

        ctx.projects.sort(key=lambda p: len(str(p.source_dir)), reverse=True)
        changed = set()

        for file in changed_files:
            for proj in ctx.projects:
                project_path = os.path.join(
                    relative_realm_repo_path, proj.relative_path
                ).rstrip(os.path.sep)
                project_path += os.path.sep
                if file.startswith(project_path):
                    changed.add(proj)
                    continue
        return changed

    @classmethod
    def parse_changed_files(cls, changed_files: str) -> List[str]:
        def handle_windows(p: str):
            return p.replace("/", os.sep)

        changed_files = changed_files if changed_files else ""
        return [handle_windows(f.strip()) for f in changed_files.split("\n") if f]
