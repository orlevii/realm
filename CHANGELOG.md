# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.4.1] - 2024-02-20
### Fixed
* fix: issue with realm run (https://github.com/orlevii/realm/pull/36)

## [0.4.0] - 2024-02-20
### Changed
* feat: parallel tasks now runs according to topology order

### Added
* On Windows, the `--scope` and `--ignore` filters can now also use `^` instead of `*` for wildcard matching. This change accommodates how glob patterns are resolved on Windows.

### Fixed
* Correctly detect dependencies under `tool.poetry.group.*.dependencies`.
* Fixed issue with identifying affected projects.

## [0.3.0] - 2024-02-05
### Added
* support for group dependencies (https://github.com/orlevii/realm/pull/16)

### Changed
* click 8.* support (https://github.com/orlevii/realm/pull/14)

## [0.2.0] - 2024-01-20
### Fixed
* a filtering bug caused with projects that have the same prefix (https://github.com/orlevii/realm/pull/11)

### Changed
* dropped python 3.6, 3.7 support
* upgraded dependencies

## [0.1.0.rc0] - 2021-04-10
First version of realm
