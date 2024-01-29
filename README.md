## Realm

`realm` is a Python open-source tool inspired by `lerna` and `nx`. It is designed to manage multiple Python packages/projects within the same Git repository. The primary focus is on running tasks across all projects in the repository and performing tasks on projects affected by specific changes.

[![Build Status](https://github.com/orlevii/realm/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/orlevii/realm/actions/workflows/build.yml?query=branch%3Amain)

## Features

- **Poetry Integration:** `realm` is built to manage projects that use `poetry`. Therefore, each project within the repository should have a `pyproject.toml` file.

- **Dependency Management:** `realm` scans the `pyproject.toml` files to identify local `path` dependencies managed within the repository. If a project depends on a library, changes to that library will be considered when determining affected projects.

## Commands

- **realm init:** Initializes a new `realm` repository.
- **realm install:** Executes `poetry install` on all projects.
- **realm ls:** Lists all projects managed by `realm`.
- **realm run:** Executes a command on all projects.
- **realm task:** Runs a `poetry` task on projects containing that task (requires `poethepoet`).

### Filtering

You can apply filters to affect only specific projects. For example, to install only changed projects:

```bash
$ realm install --since origin/master
```

Available filters:

* **--since:** Includes only projects changed since the specified reference.
* **--scope:** Includes only projects that match the given pattern.
* **--ignore:** Excludes projects that match the given pattern.
* **--match:** Filters projects by a field specified in the pyproject.toml file.

Feel free to contribute, report issues, or suggest improvements. Happy coding with `realm`!
