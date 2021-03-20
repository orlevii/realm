import os
from pathlib import Path

import toml

PYPROJECT_FILE = 'pyproject.toml'


class Project:
    def __init__(self, source_dir, root_dir):
        self.source_dir = Path(source_dir)
        self.name = os.path.basename(source_dir)
        self.relative_path = source_dir[len(root_dir):].lstrip('/')

        toml_path = str(self.source_dir.joinpath(PYPROJECT_FILE))
        self.pyproject = toml.load(toml_path)

    @property
    def version(self) -> str:
        return self.pyproject['tool']['poetry']['version']

    @property
    def package_name(self) -> str:
        return self.pyproject['tool']['poetry']['name']

    @property
    def dependencies(self):
        all_dependencies = dict(self.pyproject['tool']['poetry']['dev-dependencies'])
        all_dependencies.update(self.pyproject['tool']['poetry']['dependencies'])

        return all_dependencies

    def has_task(self, task_name) -> bool:
        tasks = self.pyproject['tool'].get('poe', {}).get('tasks', {})
        return task_name in tasks

    def execute_cmd(self, cmd):
        full_cmd = f'cd "{self.source_dir}" && {cmd}'
        if os.getenv('VIRTUAL_ENV'):
            full_cmd = f'source deactivate && {full_cmd}'
        print(full_cmd)

        status = os.system(full_cmd)
        if status != 0:
            raise RuntimeError(f'Failed running command: {cmd}. '
                               f'project: {os.path.basename(self.source_dir)}')

    def __repr__(self):
        return self.package_name
