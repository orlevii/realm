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
    changed_files = changed_files if changed_files else ''
    changed_files = [f for f in changed_files.split('\n') if f]
    ctx.projects.sort(key=lambda p: len(str(p.source_dir)), reverse=True)
    changed = set()

    for file in changed_files:
        for proj in ctx.projects:
            if file.startswith(proj.relative_path):
                changed.add(proj)
                continue
    return changed
