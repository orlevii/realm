import shutil
import sys
from pathlib import Path

import click
import toml

from realm.cli.realm_command import RealmCommand
from realm.entities.project import Project


class BuildCommand(RealmCommand[dict]):
    NAME = "build"
    HELP_MESSAGE = """
    Runs poetry build on all projects, it will replace path-dependencies with their current version in the workspace
    """

    def run(self):
        self._run_in_pool(self._build)

    def _build(self, project: Project):
        bak_file = project.pyproject_toml_path.with_name("_bak_realm_pyproject.toml")

        try:
            self._prep_build(project, bak_file)

            out = project.execute_cmd("poetry build")
            if out:
                click.echo(out)
        except Exception as e:
            click.echo(e, err=True)
            sys.exit(1)
        finally:
            if bak_file.is_file():
                shutil.copy2(bak_file, project.pyproject_toml_path)
                bak_file.unlink()

    def _prep_build(self, project: Project, bak_file: Path):
        tmp_pyproject = dict(project.pyproject)

        dependencies = self.ctx.dependency_graph.project_deps[project]
        if not any(dependencies):
            return

        shutil.copy2(project.pyproject_toml_path, bak_file)
        for dep_group, dep_name, dep_version in self._iterate_dependencies(
            tmp_pyproject
        ):
            for proj_dep in dependencies:
                if project.is_dependency(proj_dep, dep_version):
                    dep_group[dep_name] = f"^{proj_dep.version}"
                    break

        with project.pyproject_toml_path.open("w") as f:
            toml.dump(tmp_pyproject, f)

    @staticmethod
    def _iterate_dependencies(pyporject: dict):
        def iterate_dict(d: dict):
            for k, v in d.items():
                yield d, k, v

        tool_poetry = pyporject["tool"]["poetry"]
        for _, group_value in tool_poetry.get("group", {}).items():
            grp = group_value.get("dependencies", {})
            yield from iterate_dict(grp)
        yield from iterate_dict(tool_poetry.get("dev-dependencies", {}))
        yield from iterate_dict(tool_poetry.get("dependencies", {}))

    @staticmethod
    def _is_path_dependency():
        pass
