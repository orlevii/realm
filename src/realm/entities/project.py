import os
from pathlib import Path

import toml
from realm.utils.child_process import ChildProcess

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

    def extract_field(self, toml_path: str):
        parts = toml_path.split('.')
        current = self.pyproject
        for p in parts:
            current = current.get(p, {})
        if bool(current):
            return current
        return None

    @property
    def dependencies(self):
        all_dependencies = dict(self.pyproject['tool']['poetry']['dev-dependencies'])
        all_dependencies.update(self.pyproject['tool']['poetry']['dependencies'])

        return all_dependencies

    def has_task(self, task_name) -> bool:
        tasks = self.pyproject['tool'].get('poe', {}).get('tasks', {})
        return task_name in tasks

    def execute_cmd(self, cmd, **kwargs):
        full_cmd = cmd
        env = dict(os.environ)
        current_venv = os.getenv('VIRTUAL_ENV', os.getenv('CONDA_PREFIX'))
        if current_venv:
            path_env = os.environ.get('PATH', '')
            # Remove venv from path
            env['PATH'] = ':'.join([e for e
                                    in path_env.split(':')
                                    if current_venv not in e])

        try:
            params = dict(stdout=None,
                          stderr=None,
                          shell=True,
                          env=env,
                          cwd=self.source_dir)
            params.update(kwargs)
            return ChildProcess.run(full_cmd,
                                    **params)
        except RuntimeError as e:
            msg = f'{str(e)}\nproject: {os.path.basename(self.source_dir)}'
            raise RuntimeError(msg)

    def __repr__(self):
        return self.package_name
