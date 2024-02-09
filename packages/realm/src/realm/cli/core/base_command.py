import abc
import re
import sys
from typing import Generic, List, Optional, Type, TypeVar

import click

T = TypeVar("T")


def _strip_indent(s):
    if s is None:
        return None
    pattern = re.compile(r"^[ \t]*(?=\S)", re.MULTILINE)
    indent = min(len(spaces) for spaces in pattern.findall(s))

    if not indent:
        return s

    return re.sub(re.compile(r"^[ \t]{%s}" % indent, re.MULTILINE), "", s)


class BaseCommand(Generic[T]):
    CLICK_COMMAND_CLS = click.Command
    NAME: str = ""
    HELP_MESSAGE: Optional[str] = None
    PARAMS: List[click.Parameter] = []
    DEPRECATED: bool = False
    SCHEMA: Type[T] = dict

    def __init__(self, ctx, **kwargs):
        self.ctx = ctx
        self.params: T = self.SCHEMA(**kwargs)
        self._params: dict = kwargs

    @classmethod
    def to_command(cls):
        def callback_fn(**kwargs):
            from realm.cli.app_context_creator import AppContextCreator
            cmd = cls(AppContextCreator.init_context(), **kwargs)
            code = cmd.run()
            if code is not None:
                sys.exit(code)

        return cls.CLICK_COMMAND_CLS(
            name=cls.NAME,
            params=cls.PARAMS,
            callback=callback_fn,
            help=_strip_indent(cls.HELP_MESSAGE),
            deprecated=cls.DEPRECATED,
        )

    @abc.abstractmethod
    def run(self):  # type: Optional[int]
        """
        Runs the command
        :return: Exit code
        """
        raise NotImplementedError()
