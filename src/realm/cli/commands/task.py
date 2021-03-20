import click
from realm.cli.realm_command import RealmCommand


class TaskCommand(RealmCommand[dict]):
    NAME = 'task'
    PARAMS = [
        click.Argument(['task_name'], type=click.STRING)
    ]

    def _filter_projects(self):
        super()._filter_projects()
        task_name = self.params['task_name']
        self.ctx.projects = [p for p
                             in self.ctx.projects
                             if p.has_task(task_name)]

    def run(self):
        task_name = self.params['task_name']
        failed_projects = []
        std_outs = []
        for project in self.ctx.projects:
            click.echo(f'Running task {task_name} for: {project.name}')
            try:
                out = project.execute_cmd(f'poetry run poe {task_name}')
                if out:
                    std_outs.append(out)
            except RuntimeError as e:
                click.echo(e, err=True)
                failed_projects.append(project)

        if any(failed_projects):
            names = [p.name for p in failed_projects]
            formatted_names = ', '.join(names)
            raise RuntimeError(f'Task {task_name} failed for projects: {formatted_names}')

        if any(std_outs):
            # For stdout capturing
            outs = '\n'.join(std_outs)
            click.echo(outs)
