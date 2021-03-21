import click

from .core.params import GlobalOption


class RealmFormatter(click.HelpFormatter):
    def __init__(self, headers_color=None, options_color=None, *args, **kwargs):
        self.headers_color = headers_color
        self.options_color = options_color
        super().__init__(*args, **kwargs)

    def write_usage(self, prog, args='', prefix='Usage: '):
        colorized_prefix = click.style(prefix, fg=self.headers_color)
        super().write_usage(prog,
                            args,
                            prefix=colorized_prefix)

    def write_heading(self, heading):
        self.write(click.style('', fg=self.headers_color, reset=False))
        super().write_heading(heading)
        self.write(click.style('', reset=True))

    def write_dl(self, rows, **kwargs):
        colorized_rows = [(click.style(row[0], fg=self.options_color), row[1])
                          for row
                          in rows]
        super().write_dl(colorized_rows, **kwargs)


class RealmFormatHelpMixin(click.Command):
    def get_help(self, ctx):
        formatter = RealmFormatter(
            width=500,
            max_width=ctx.max_content_width,
            headers_color='yellow',
            options_color='bright_blue')
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip('\n')

    def format_options(self, ctx, formatter):
        """Writes all the options into the formatter if they exist."""
        opts = []
        global_opts = []
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None:
                if self.__is_global_option(param):
                    global_opts.append(rv)
                else:
                    opts.append(rv)

        if global_opts:
            with formatter.section("Global Options"):
                formatter.write_dl(global_opts)

        if opts:
            with formatter.section("Options"):
                formatter.write_dl(opts)

    @staticmethod
    def __is_global_option(opt: click.Option):
        return isinstance(opt, GlobalOption) or opt.name == 'help'
