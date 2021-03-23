import os
from typing import List

from realm.entities import Project

from ..entities.context import RealmContext
from ..utils.child_process import ChildProcess


def apply_since_filters(ctx: RealmContext, since):
    changed_projects = get_changed_projects(ctx, since)
    dependent = set()
    for proj in ctx.projects:
        if is_project_affect_by_change(proj, changed_projects):
            dependent.add(proj)

    dependent = dependent.union(changed_projects)

    ctx.projects = dependent


def is_project_affect_by_change(project, changed_projects):
    changed_dependencies = [
        p
        for p
        in changed_projects
        if is_dependent(project, p)
    ]
    return any(changed_dependencies)


def is_dependent(project: Project, changed_project: Project):
    dependency = project.dependencies.get(changed_project.package_name)
    if dependency is None:
        return False
    if not isinstance(dependency, dict):
        # Path dependency is a dict
        return False
    dependency_path = dependency.get('path')
    if dependency_path is None:
        return False
    return project.source_dir.joinpath(dependency_path).resolve() == changed_project.source_dir


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
