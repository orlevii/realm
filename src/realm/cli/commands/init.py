import json
import pathlib

from realm.cli.realm_command import RealmCommand
from realm.utils.child_process import ChildProcess

INIT_DATA = {
    "projects": [
        "packages/*"
    ]
}


class InitCommand(RealmCommand[dict]):
    NAME = 'init'
    HELP_MESSAGE = """
    Initializes a new realm repo
    """

    def run(self):
        self.create_realm_json()
        self.create_stub_package()

    @staticmethod
    def create_realm_json():
        with open('realm.json', 'w') as f:
            json.dump(INIT_DATA, f, indent=2)

    @staticmethod
    def create_stub_package():
        packages_dir = pathlib.Path('packages')
        if not packages_dir.is_dir():
            packages_dir.mkdir(parents=True)
        ChildProcess.run('poetry new pgk --src', cwd=packages_dir.absolute())
