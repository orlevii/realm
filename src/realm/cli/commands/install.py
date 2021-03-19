from realm.cli.realm_command import RealmCommand


class InstallCommand(RealmCommand[dict]):
    NAME = 'install'

    def run(self):
        for project in self.ctx.projects:
            project.execute_cmd('poetry install')
