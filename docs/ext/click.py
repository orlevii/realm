from __future__ import annotations

from typing import Iterator
from unittest.mock import patch

import click
from mkdocs_click import MKClickExtension
from mkdocs_click._docs import _format_table_option_row, _make_table_options
from realm.cli.core.params import GlobalOption

original_fn = _make_table_options


def _is_global_option(opt: click.Option):
    return isinstance(opt, GlobalOption)


def make_table_options_patch(
        ctx: click.Context, show_hidden: bool = False
) -> Iterator[str]:
    options = [
        param
        for param in ctx.command.get_params(ctx)
        if isinstance(param, click.Option)
    ]
    options = [option for option in options if not option.hidden or show_hidden]
    if ctx.command.name:
        options = [option for option in options if not _is_global_option(option)]

    global_options_rows = [
        _format_table_option_row(option)
        for option in options
        if _is_global_option(option)
    ]
    options_rows = [
        _format_table_option_row(option)
        for option in options
        if not _is_global_option(option)
    ]

    if not ctx.command.name:
        global_options_rows += options_rows
        options_rows = []

    if any(global_options_rows):
        yield "**Global Options:**"
        yield ""
        yield "| Name | Type | Description | Default |"
        yield "| ---- | ---- | ----------- | ------- |"
        yield from global_options_rows
        yield ""

    if any(options_rows):
        yield "**Options:**"
        yield ""
        yield "| Name | Type | Description | Default |"
        yield "| ---- | ---- | ----------- | ------- |"
        yield from options_rows
        yield ""


func_to_patch = f"{_make_table_options.__module__}.{_make_table_options.__name__}"
mock = patch(func_to_patch, side_effect=make_table_options_patch)
mock.start()


class MyMKClickExtension(MKClickExtension):
    pass


def makeExtension():  # noqa: N802
    return MyMKClickExtension()
