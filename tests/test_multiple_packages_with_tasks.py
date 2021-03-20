import unittest

from realm.cli.application import Application
from realm.cli.commands.install import InstallCommand
from realm.cli.commands.ls import LsCommand
from realm.cli.commands.task import TaskCommand
from realm.entities import Config, RealmContext

from tests.common import get_tests_root_dir, captured_output

REPO_DIR = get_tests_root_dir().joinpath('scenarios/multiple_packages_with_tasks')


class TestCommands(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # Create config once
        cls.cfg = Config.from_file(realm_json_file=str(REPO_DIR.joinpath('realm.json')))

    def setUp(self) -> None:
        # Create context every test
        self.ctx = RealmContext(config=self.cfg,
                                projects=Application.get_projects(self.cfg))

    def test_scan(self):
        found = len(self.ctx.projects)
        self.assertEqual(found, 1)

    def test_ls(self):
        cmd = LsCommand(self.ctx)
        with captured_output() as (out, _):
            cmd.run()
        output = out.getvalue().strip()
        self.assertEqual(output, 'pgk@0.1.0')

    def test_task_install(self):
        install_cmd = InstallCommand(self.ctx)
        task_cmd = TaskCommand(self.ctx, task_name='test')

        self.assertEqual(len(task_cmd.ctx.projects), 1)

        with captured_output(stderr=False) as (out, _):
            install_cmd.run()
            task_cmd.run()

        output = out.getvalue()
        self.assertIn('Installing the current project: pgk', output)
        self.assertIn('Poe => python -m unittest discover -s tests -v -p "test_*.py"', output)
