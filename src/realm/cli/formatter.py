import click


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
