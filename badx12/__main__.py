# -*- coding: utf-8 -*-

"""Main module."""
import logging
import sys

import click

from .commands import parse
from .common.click import add_commands


@click.group()
@click.option(
    "-l",
    "--log",
    default="INFO",
    help="Set the logging level",
    type=click.Choice(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]),
)
def cli(log):
    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s",
        level=log,
    )


add_commands(cli, (parse,))

if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
