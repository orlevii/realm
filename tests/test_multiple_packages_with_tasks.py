import unittest

from realm.cli.application import Application
from realm.cli.commands.install import InstallCommand
from realm.cli.commands.ls import LsCommand
from realm.cli.commands.task import TaskCommand
from realm.entities import Config, RealmContext
from realm.utils.child_process import ChildProcess

from tests.common import get_tests_root_dir, captured_output

REPO_DIR = get_tests_root_dir().joinpath("scenarios/multiple_packages_with_tasks")


class TestCommands(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Create config once
        cls.cfg = Config.from_file(realm_json_file=str(REPO_DIR.joinpath("realm.json")))

    def setUp(self) -> None:
        # Create context every test
        self.ctx = RealmContext(
            config=self.cfg, projects=Application.get_projects(self.cfg)
        )

    def test_scan(self):
        found = len(self.ctx.projects)
        self.assertEqual(found, 2)

    def test_ls(self):
        cmd = LsCommand(self.ctx)
        with captured_output() as (out, _):
            cmd.run()
        output = out.getvalue().strip()
        self.assertIn("pkg@0.1.0", output)
        self.assertIn("pkg_with_groups@0.1.0", output)

    def test_task_install(self):
        install_cmd = InstallCommand(self.ctx)
        task_cmd = TaskCommand(self.ctx, task_name="test")

        self.assertEqual(len(task_cmd.ctx.projects), 1)

        with captured_output(stderr=False) as (out, _):
            install_cmd.run()
            task_cmd.run()

        output = out.getvalue()
        self.assertIn("Installing the current project: pkg", output)
        self.assertIn(
            'Poe => python -m unittest discover -s tests -v -p "test_*.py"', output
        )

    def test_git_diff(self):
        cmd = LsCommand(self.ctx, since=".")
        with captured_output() as (out, _):
            cmd.run()
        output = out.getvalue().strip()
        self.assertEqual(output, "")

    def test_git_diff_with_change(self):
        pkg_proj = [p for p in self.ctx.projects if p.name == "pkg"][0]
        try:
            with pkg_proj.source_dir.joinpath("pyproject.toml").open("a") as f:
                print("", file=f)

            cmd = LsCommand(self.ctx, since=".")

            with captured_output() as (out, _):
                cmd.run()
            output = out.getvalue().strip()
            self.assertEquals("pkg@0.1.0", output)
        finally:
            ChildProcess.run(f"git checkout {pkg_proj.source_dir}")

    def test_scope_filter(self):
        cmd = LsCommand(self.ctx, scope=["p*"], ignore=["*with*"])
        with captured_output() as (out, _):
            cmd.run()
        output = out.getvalue().strip()
        self.assertEqual(output, "pkg@0.1.0")

    def test_ignore_filter(self):
        cmd = LsCommand(self.ctx, ignore=["p*"])
        with captured_output() as (out, _):
            cmd.run()
        output = out.getvalue().strip()
        self.assertEqual(output, "")

    def test_match_filter(self):
        cmd = LsCommand(self.ctx, match=["labels.type=package"])
        with captured_output() as (out, _):
            cmd.run()
        output = out.getvalue().strip()
        self.assertEqual(output, "pkg@0.1.0")
