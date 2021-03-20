import unittest

from realm.cli.application import Application
from realm.cli.commands.ls import LsCommand
from realm.entities import Config, RealmContext

from tests.common import get_tests_root_dir, captured_output

REPO_DIR = get_tests_root_dir().joinpath('scenarios/multiple_packages_with_tasks')


class TestCommands(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = Config.from_file(realm_json_file=str(REPO_DIR.joinpath('realm.json')))
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
