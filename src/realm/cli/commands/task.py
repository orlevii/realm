import click
from realm.cli.realm_command import RealmCommand


class TaskCommand(RealmCommand[dict]):
    NAME = 'task'
    PARAMS = [
        click.Argument(['task_name'], type=click.STRING)
    ]

    def run(self):
        task_name = self.params['task_name']
        failed_projects = []
        for project in self.ctx.projects:
            if project.has_task(task_name):
                click.echo(f'Running task {task_name} for: {project.name}')
                try:
                    project.execute_cmd(f'poetry run poe {task_name}')
                except RuntimeError as e:
                    click.echo(e)
                    failed_projects.append(project)

        if any(failed_projects):
            names = [p.name for p in failed_projects]
            formatted_names = ', '.join(names)
            raise RuntimeError(f'Task {task_name} failed for projects: {formatted_names}')
