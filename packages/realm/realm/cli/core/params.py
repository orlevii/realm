import click


class GlobalOption(click.Option):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
