# -*- coding: utf-8 -*-
from collections import Iterable
from typing import Iterable as IterableType

import click


def add_commands(click_group: click.core.Group, commands: IterableType) -> None:
    if not isinstance(click_group, click.core.Group):
        raise TypeError(
            f"add_commands() expects click.core.Group for click_group, got {type(click_group)}"
        )

    if not isinstance(commands, Iterable):
        raise TypeError(
            f"add_commands() expects an Iterable type for commands, got {type(commands)}"
        )

    for command in commands:
        if not isinstance(command, click.core.Command) and not isinstance(
            command, click.core.Group
        ):
            raise TypeError(
                f"commands must be of type click.core.Command or click.core.Group, got {type(command)}"
            )

        click_group.add_command(command)
