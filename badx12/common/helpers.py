# -*- coding: utf-8 -*-
from typing import Generator, Iterable


def lookahead(iterable: Iterable) -> Generator:
    it = iter(iterable)
    last = next(it)

    for val in it:
        yield last, True
        last = val

    yield last, False
