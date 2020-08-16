# -*- coding: utf-8 -*-
import pprint as pp

from .interchange import Interchange
from .settings import DocumentConfiguration, DocumentSettings
from .validators import ValidationReport


class EDIDocument:
    """
    An EDI X12 Document
    """

    def __init__(self) -> None:
        self.text: str = ""
        self.config: DocumentConfiguration = DocumentConfiguration(
            version=DocumentSettings.version,
            element_separator=DocumentSettings.element_separator,
            segment_terminator=DocumentSettings.segment_terminator,
            sub_element_separator=DocumentSettings.sub_element_separator,
        )

        self.interchange: Interchange = Interchange()

    def format_as_edi(self) -> str:
        """Format this document as EDI and return it as a string"""
        return self.interchange.format_as_edi(self.config)

    def validate(self) -> ValidationReport:
        """Validate this document and return a validation report"""
        report: ValidationReport = ValidationReport()
        self.interchange.validate(report)
        return report

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "config": self.config.to_dict(),
            "interchange": self.interchange.to_dict(),
        }

    def __repr__(self) -> str:
        _pp: pp.PrettyPrinter = pp.PrettyPrinter(indent=2)
        return _pp.pformat(self.to_dict())
