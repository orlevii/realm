## Realm

**realm** is a CLI tool written in Python aimed at simplifying the development and maintenance of multiple Python projects within the same repository with a particular focus on projects structured using Poetry.

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

**Available filters:**
* <code>--since</code> - Includes only projects changed since the specified reference.
* <code>--scope</code> - Includes only projects that match the given pattern.
* <code>--ignore</code> - Excludes projects that match the given pattern.
* <code>--match</code> - Filters projects by a field specified in the pyproject.toml file.

## Documentation
For more information on available commands and usage, refer to the [documentation](https://orlevii.github.io/realm/).

## Contribution
Contributions to `realm` are welcome! If you encounter any issues or have suggestions for improvements, please open an issue.
