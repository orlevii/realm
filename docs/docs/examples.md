# Examples

## Intro
Let's look at the following repository structure:

```
.
├── packages
│   ├── pkg_a
│   │   ├── README.md
│   │   ├── poetry.lock
│   │   ├── pyproject.toml
│   │   ├── src
│   │   │   └── pkg_a
│   │   └── tests
│   │       └── __init__.py
│   ├── pkg_b
│   │   ├── README.md
│   │   ├── poetry.lock
│   │   ├── pyproject.toml
│   │   ├── src
│   │   │   └── pkg_b
│   │   └── tests
│   ├── pkg_c
│   │   ├── README.md
│   │   ├── poetry.lock
│   │   ├── pyproject.toml
│   │   ├── src
│   │   │   └── pkg_c
│   │   └── tests
└── realm.json
```
With the following `realm.json` file:

```json
{
  "projects": [
    "packages/*"
  ]
}
```
`realm.json` is a simple file that tells realm CLI where to look for projects. In this case, it's looking for projects in the `packages` directory.

## Filtering

When working with a repository with many projects, you may want to focus on specific parts rather than applying commands to the entire project. Realm offers filtering options to help you do just that.

### --since

For instance, if you only want to run tests on projects affected by recent changes, you can use:

```bash
realm task test --since main
```

This command runs the `test` task only on projects affected by recent changes.

If `pkg_a` and `pkg_b` have been modified in our branch. The `test` task will only run on those two projects.

#### Affected Projects
Let's say that `pkg_a` depends on `pkg_c`:
```toml
[tool.poetry]
name = "pkg_a"
# ...

[tool.poetry.dependencies]
pkg_c = { path = "../pkg_c", develop = true }
```
In that case, if `pkg_c` is modified, `pkg_a` will also be considered affected and the `test` task will run on both projects.

### --scope

You can use simple wildcards to filter projects:

```bash
realm ls --scope "*_a"
```

This command displays projects that end with `_a`.
In our case, it will only display `pkg_a`.

???+ note "On Windows"
    On Windows, you can also use `^` instead of `*` due to how wildcards are handled:
    
    ```powershell
    realm ls --scope "^_a"
    ```


### --ignore

Similar to '--scope', but excludes projects:

```bash
realm ls --ignore "^_a"
```

This command shows projects that do not end with `_a`.

In our case, it will display `pkg_b` and `pkg_c`.

### --match

This filter allows you to specify any field from the 'pyproject.toml' file.

For example, if you define:

```toml
[tool.poetry]
name = "pkg_b"

[tool.realm.labels]
my_field = "my_value"
```

To match that project, you can then run:

```bash
realm ls --match labels.my_field=my_value
```

This command will display `pkg_b`.

## Building
Realm helps you when you have dependencies between projects.

In our example, `pkg_a` depends on `pkg_c`. If you run:

```bash
realm build
```
The output `.whl` file for `pkg_a` will no longer be dependent on the local editable installation of `pkg_c`, but rather on the current version of `pkg_c` that is in your workspace.

```toml
[tool.poetry]
name = "pkg_c"
version = "1.1.0"
```

The `pkg_a`'s `pyproject.toml` file that will be used for building will be:
```toml
[tool.poetry]
name = "pkg_a"
# ...

[tool.poetry.dependencies]
pkg_c = "^1.1.0" # Instead of { path = "../pkg_c", develop = true }
```

### Publishing

When you're ready to publish your projects, you can use the `publish` command from `poetry`:

```bash
realm build
realm run -- poetry publish
```
This will build the projects and then run `poetry publish` on each of them.
