# Commands

## Global Options

Realm commands can accept the following global options:

- **--since**: Includes only projects affected by a change since the specified reference.
- **--all**: Includes all projects if no projects were changed when using the --since filter.
- **--scope**: Includes only projects that match the given wilcard pattern.
- **--ignore**: Filters out projects that match the given wildcard pattern.
- **--match**: Filters by a field specified in `pyproject.toml`.

## cli

### init

Initializes a new `realm` repository.

This command will create a `realm.json` and an empty directory structure for projects.

### install

Executes `poetry install` on all projects.

### ls

Lists all projects managed by `realm`.

**Options:**

* **--paths** - Prints relative paths of the projects.

### run

Executes a command on all projects.

**Example:**
```bash
realm run -- pwd
```
This command will execute `pwd` from each project.

### task

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

## Filtering

In most cases, you wouldn't like to build/test or do anything on the entire repository, realm allows filtering to make sure you run your commands only on what's needed.

### since

For example, if we would like to run tests only on affected projects by our changes, we could do
```bash
realm task test --since main
```

This command will filter only affected projects by our changes and run the `test` task defined in each `pyproject.toml` of the affected projects.

### scope
Allows filtering by wildcard

```bash
realm ls --scope "r*"
```
Will output only projects that start with the letter `r`.

In windows, The CLI will also accept `^` as the `*` because of the way wildcards are resoved there.
```powershell
realm ls --scope "r^"
```

### ignore
Same as `--scope`, but will filter out.
```bash
realm ls --ignore "r*"
```
Will output only projects that **DO NOT** start with the letter `r`.

### match
With this filter, you can filter by ANY field specified in the `pyproject.toml`

You can also define for example:

```toml
[tool.realm.labels]
my_field = "my_value"
```

And then run:
```bash
realm ls --match labels.my_field=my_value
```
