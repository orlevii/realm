import sys

import click

from realm.cli.realm_command import RealmCommand


class TaskCommand(RealmCommand[dict]):
    NAME = "task"
    HELP_MESSAGE = """
    Runs a poe task on all projects containing this task
    """
    PARAMS = [click.Argument(["task_name"], type=click.STRING)]

    def _filter_projects(self):
        super()._filter_projects()
        task_name = self.params["task_name"]
        self.ctx.projects = [p for p in self.ctx.projects if p.has_task(task_name)]

    def run(self):
        task_name = self.params["task_name"]
        failed_projects = []

        self._run_in_pool(
            self.execute_task, task_name=task_name, failed_projects=failed_projects
        )

        if any(failed_projects):
            names = [p.name for p in failed_projects]
            formatted_names = ", ".join(names)
            msg = f"Task {task_name} failed for projects: {formatted_names}"
            click.echo(msg, err=True)
            sys.exit(1)

    @staticmethod
    def execute_task(project, task_name, failed_projects):
        click.echo(f"Running task {task_name} for: {project.name}")
        try:
            out = project.execute_cmd(f"poetry run poe {task_name}")
            if out:
                click.echo(out)
        except RuntimeError as e:
            click.echo(e, err=True)
            failed_projects.append(project)
