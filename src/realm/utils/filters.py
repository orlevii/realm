import os
from typing import List

from ..entities.context import RealmContext
from ..utils.child_process import ChildProcess


def apply_since_filters(ctx: RealmContext, since):
    changed_projects = get_changed_projects(ctx, since)
    dependent = set()
    for proj in ctx.projects:
        changed_dep = [p for p in changed_projects if p.package_name in proj.dependencies.keys()]
        if any(changed_dep):
            dependent.add(proj)

    dependent = dependent.union(changed_projects)

    ctx.projects = dependent


def get_changed_projects(ctx: RealmContext, since):
    changed_files = ChildProcess.run(f'git diff --name-only {since}')
    git_root = ChildProcess.run('git rev-parse --show-toplevel')
    git_root = git_root.strip() if git_root else ''

    relative_realm_repo_path = ctx.config.root_dir[len(git_root):].lstrip(os.sep)

    changed_files = parse_changed_files(changed_files)

    ctx.projects.sort(key=lambda p: len(str(p.source_dir)), reverse=True)
    changed = set()

    for file in changed_files:
        for proj in ctx.projects:
            project_path = os.path.join(relative_realm_repo_path,
                                        proj.relative_path)
            print('----')
            print('realm:', relative_realm_repo_path)
            print('proj_relative:', proj.relative_path)
            print('joined:', project_path)
            print('changed_file:', file)
            print('----')
            if file.startswith(project_path):
                changed.add(proj)
                continue
    return changed


def parse_changed_files(changed_files: str) -> List[str]:
    def handle_windows(p: str):
        return p.replace('/', os.sep)

    changed_files = changed_files if changed_files else ''
    return [
        handle_windows(f.strip())
        for f
        in changed_files.split('\n')
        if f
    ]
