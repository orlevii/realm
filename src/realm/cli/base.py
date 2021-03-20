import abc
import re
import sys
from typing import Optional, List, Generic, TypeVar, Type

import click

T = TypeVar('T')


def _strip_indent(s):
    if s is None:
        return None
    pattern = re.compile(r'^[ \t]*(?=\S)', re.MULTILINE)
    indent = min(len(spaces) for spaces in pattern.findall(s))

    if not indent:
        return s

    return re.sub(re.compile(r'^[ \t]{%s}' % indent, re.MULTILINE), '', s)


class BaseCommand(Generic[T]):
    NAME: str = ''
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
        def callback_fn(ctx, **kwargs):
            cmd = cls(ctx=ctx.obj,
                      **kwargs)
            code = cmd.run()
            if code is not None:
                sys.exit(code)

        return click.Command(name=cls.NAME,
                             params=cls.PARAMS,
                             callback=click.pass_context(callback_fn),
                             help=_strip_indent(cls.HELP_MESSAGE),
                             deprecated=cls.DEPRECATED)

    @abc.abstractmethod
    def run(self):  # type: Optional[int]
        """
        Runs the command
        :return: Exit code
        """
        pass
