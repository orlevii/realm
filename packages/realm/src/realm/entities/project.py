import os
from functools import cached_property
from pathlib import Path

import toml

from realm.utils.child_process import ChildProcess

PYPROJECT_FILE = "pyproject.toml"


class Project:
    def __init__(self, source_dir, root_dir):
        self.source_dir = Path(source_dir)
        self.name = os.path.basename(source_dir)
        self.relative_path = source_dir[len(root_dir) :].lstrip(os.sep)

        self.pyproject_toml_path = self.source_dir.joinpath(PYPROJECT_FILE)
        self.pyproject = toml.load(self.pyproject_toml_path)

    @property
    def version(self) -> str:
        return self.pyproject["tool"]["poetry"]["version"]

    @property
    def package_name(self) -> str:
        return self.pyproject["tool"]["poetry"]["name"]

    def extract_field(self, toml_path: str):
        parts = toml_path.split(".")
        current = self.pyproject
        for p in parts:
            current = current.get(p, {})
        if bool(current):
            return current
        return None

    @cached_property
    def dependencies(self):
        tool_poetry = self.pyproject["tool"]["poetry"]
        all_dependencies = {}
        for _, group_value in tool_poetry.get("group", {}).items():
            all_dependencies.update(group_value.get("dependencies", {}))

        all_dependencies.update(tool_poetry.get("dev-dependencies", {}))
        all_dependencies.update(tool_poetry["dependencies"])

        return all_dependencies

    def has_task(self, task_name) -> bool:
        tasks = self.pyproject["tool"].get("poe", {}).get("tasks", {})
        return task_name in tasks

    def execute_cmd(self, cmd, **kwargs):
        full_cmd = cmd
        env = self._create_env()

        try:
            params = {
                "stdout": None,
                "stderr": None,
                "shell": True,
                "env": env,
                "cwd": self.source_dir,
            }
            params.update(kwargs)
            return ChildProcess.run(full_cmd, **params)
        except RuntimeError as e:
            msg = f"{e!s}\nproject: {os.path.basename(self.source_dir)}"
            raise RuntimeError(msg) from e

    def is_dependent_on(self, other: "Project") -> bool:
        dependency = self.dependencies.get(other.package_name)
        return self.is_dependency(other, dependency)

    def is_dependency(self, other: "Project", dependency: dict) -> bool:
        if dependency is None:
            return False
        if not isinstance(dependency, dict):
            # Path dependency is a dict
            return False
        dependency_path = dependency.get("path")
        if dependency_path is None:
            return False
        dependency_path = dependency_path.replace("/", os.sep)
        return self.source_dir.joinpath(dependency_path).resolve() == other.source_dir

    def __repr__(self):
        return self.package_name

    def _create_env(self):
        env = dict(os.environ)
        current_venv = os.getenv("VIRTUAL_ENV", os.getenv("CONDA_PREFIX"))
        if current_venv:
            path_env = os.environ.get("PATH", "")
            # Remove venv from path
            env["PATH"] = ":".join(
                [e for e in path_env.split(":") if current_venv not in e]
            )
            env.pop("VIRTUAL_ENV", None)
            env.pop("CONDA_PREFIX", None)
        env["REALM_PROJECT_NAME"] = self.name
        env["REALM_PROJECT_PATH"] = str(self.source_dir)

        return env
