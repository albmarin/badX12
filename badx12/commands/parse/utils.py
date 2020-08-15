# -*- coding: utf-8 -*-
import json
import logging
import time
from pathlib import Path
from typing import Callable, Tuple

from dicttoxml import dicttoxml

logging.getLogger("dicttoxml").setLevel(logging.WARNING)


def export_file(dict_obj: dict, export_type: str, output_dir: Path) -> None:
    obj, output_path = _parse_params(dict_obj, export_type, output_dir)
    with open(output_path, "w") as f:
        if isinstance(obj, bytes):
            obj = obj.decode("utf-8")

        f.write(obj)


def _parse_params(
    dict_obj: dict, export_type: str, output_dir: Path
) -> Tuple[str, Path]:
    output_dir.mkdir(exist_ok=True)
    file_name: str = f"{int(time.time())}.{export_type.lower()}"

    func: Callable = {"json": _json, "xml": _xml}.get(export_type.lower(), _json)

    output_path: Path = output_dir / file_name
    obj: str = func(dict_obj)

    return obj, output_path


def _json(dict_obj: dict) -> str:
    return json.dumps(dict_obj, indent=2)


def _xml(dict_obj: dict) -> str:
    return dicttoxml(dict_obj)
