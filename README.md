# Realm: Multi-Project Python Build Tool

## Introduction
**realm** is a CLI tool written in Python aimed at simplifying the development and maintenance of multiple Python projects within the same repository with a particular focus on projects structured using Poetry.

[![Build Status](https://github.com/orlevii/realm/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/orlevii/realm/actions/workflows/build.yml?query=branch%3Amain)

## Motivation

Monorepos have become increasingly popular due to their ability to streamline dependency management, enhance code reusability, and simplify development processes. However, implementing monorepo structures in Python projects can be challenging, as existing tools often lack comprehensive support.

The motivation behind Realm is to facilitate development within a monorepo environment, enabling the creation of complex CI/CD pipelines and easing the management of interconnected projects.

## Why Poetry?
Poetry is a powerful tool for managing dependencies and packaging Python projects. It offers several advantages, making it well-suited for projects managed by `realm`:

Given its popularity and seamless virtual environment features, Poetry serves as an ideal tool for Realm to leverage in managing multiple projects within the same repository.

## Installation
To install `realm`, it's recommened to install in an islolated environment using `pipx`

```bash
pipx install realm
```

## Documentation
For more information on available commands and usage, refer to the [documentation](https://orlevii.github.io/realm/).

## Contribution
Contributions to `realm` are welcome! If you encounter any issues or have suggestions for improvements, please open an issue.
