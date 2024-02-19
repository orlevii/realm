# Cli Reference

## Global Options

Realm commands can accept the following global options:

- `--since`: Includes only projects affected by a change since the specified reference.
- `--all`: Includes all projects if no projects were changed when using the --since filter.
- `--scope`: Includes only projects that match the given wildcard pattern.
- `--ignore`: Filters out projects that match the given wildcard pattern.
- `--match`: Filters by a field specified in `pyproject.toml`.

## init

Initializes a new `realm` repository.

This command will create a `realm.json` and an empty directory structure for projects.

## install

Executes `poetry install` on all projects.

## ls

Lists all projects managed by `realm`.

**Options:**

* `--paths`: Prints relative paths of the projects.

## run

Executes a command on all projects.

**Example:**
```bash
realm run -- pwd
```
This command will execute `pwd` from each project.

## task

Runs a task on projects containing that task (requires `poethepoet`).

You can define tasks in `pyproject.toml`.

```toml
[tool.poe.tasks]
test = "pytest --cov=src tests"
```

You can refer to the documentation: [Poethepoet Documentation](https://poethepoet.natn.io/)

**Example:**
```bash
realm task test
```

## build

Runs poetry build on all projects, it will replace path-dependencies with their current version in the workspace. 

For example, when running the following, you can build and publish all projects in the workspace:
```bash
realm build
realm run -- poetry publish
```

## Filtering

When working with a large repository, you may want to focus on specific parts rather than applying commands to the entire project. Realm offers filtering options to help you do just that.

### since

For instance, if you only want to run tests on projects affected by recent changes, you can use:

```bash
realm task test --since main
```

This command runs the `test` task only on projects affected by recent changes

### scope

You can use wildcards to filter projects:

```bash
realm ls --scope "r*"
```

This command displays projects that start with the letter 'r'.

In Windows, you can also use '^' instead of '*' due to how wildcards are handled:

```powershell
realm ls --scope "r^"
```


### ignore

Similar to '--scope', but excludes projects:

```bash
realm ls --ignore "r*"
```

This command shows projects that do not start with the letter 'r'.

### match

This filter allows you to specify any field from the 'pyproject.toml' file.

For example, if you define:

```toml
[tool.realm.labels]
my_field = "my_value"
```

To match that project, you can then run:

```bash
realm ls --match labels.my_field=my_value
```
