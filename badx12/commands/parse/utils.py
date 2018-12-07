import json
import logging
import time

from dicttoxml import dicttoxml

logging.getLogger("dicttoxml").setLevel(logging.WARNING)


def export_file(dict_obj, export_type=None, output_dir=None):
    obj, output_path = _parse_params(dict_obj, export_type, output_dir)
    with open(output_path, "w") as f:
        if isinstance(obj, bytes):
            obj = obj.decode("utf-8")

        f.write(obj)


def _parse_params(dict_obj, export_type, output_dir):
    output_dir.mkdir(exist_ok=True)
    file_name = f"{int(time.time())}.{export_type.lower()}"

    func = {"json": _json, "xml": _xml}.get(export_type.lower(), "json")

    output_path = output_dir / file_name
    obj = func(dict_obj)

    return obj, output_path


def _json(dict_obj):
    return json.dumps(dict_obj, indent=2)


def _xml(dict_obj):
    return dicttoxml(dict_obj)
