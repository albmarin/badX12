import logging
from pathlib import Path

import click

import badx12.utils.errors as err
from badx12.common.paths import OUTPUT_DIR
from badx12.parser import Parser
from .utils import export_file

logger = logging.getLogger(__name__)


@click.command("parse", help="Parse an EDI file into JSON or XML")
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "-e",
    "--export_type",
    default="JSON",
    type=click.Choice(["JSON", "XML"]),
    help="Specify the file output type.",
)
@click.option(
    "-o",
    "--output_dir",
    default=None,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Specify an output directory.",
)
def parse(path, export_type, output_dir):
    path = Path(path)
    output_dir = Path(output_dir) if output_dir else OUTPUT_DIR
    files = [f for f in path.glob("*") if f.is_file()] if path.is_dir() else [path]

    for f in files:
        logger.debug(f"Parsing {f}, export as {export_type} to {output_dir}")
        try:
            parser = Parser(f)
            document = parser.document
            report = document.validate()

            if not report.is_document_valid():
                logger.error(
                    f"{f} contains the following errors. Issues: {[error.msg for error in report.error_list]}"
                )
                continue

            doc_dict = document.to_dict()
            export_file(doc_dict, export_type, output_dir)

        except (
            err.InvalidFileTypeError,
            err.FieldValidationError,
            err.SegmentCountError,
            err.IDMismatchError,
            err.SegmentTerminatorNotFoundError,
        ) as e:
            logger.error(f"{f} caused the following error. Exception: {e.msg}")
