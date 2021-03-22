## Realm
Realm is tool for managing multiple poetry projects in the same git repository.

This project took inspiration from the `lerna` project available for JavaScript

### Requirements
In order to start using realm, you first need to have [poetry](https://github.com/python-poetry/poetry) installed

### Commands
* <code>realm init</code> - Initializes a new realm repo
* <code>realm install</code> - Executes `poetry install` on all projects
* <code>realm ls</code> - Prints all projects managed
* <code>realm run</code> - Executes a command on all projects
* <code>realm task</code> - Runs a poe task on all projects containing this task (requires poethepoet)

#### Filtering
You can set up filters to affect only certain projects

For example, you can install only changed projects 
```bash
$ realm install --since origin/master
```

Available filters:
* <code>--since</code> - Includes only projects changed since the specified ref
* <code>--scope</code> - Includes only projects that match the given pattern
* <code>--ignore</code> - Filters out projects that match the given pattern
* <code>--match</code> - Filters by a field specified in `pyproject.toml`
