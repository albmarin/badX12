import pprint as pp

from badx12.utils import Interchange
from ._settings import DocumentSettings


class DocumentConfiguration:
    def __init__(
        self, version, element_separator, segment_terminator, sub_element_separator
    ):
        """Creates a new Edi Document Configuration"""
        self.version = version
        self.element_separator = element_separator
        self.segment_terminator = segment_terminator
        self.sub_element_separator = sub_element_separator

    def to_dict(self):
        return {
            "element_separator": self.element_separator,
            "segment_terminator": self.segment_terminator,
            "sub_element_separator": self.sub_element_separator,
            "version": self.version,
        }


class ValidationReport:
    def __init__(self):
        self.error_list = []

    def add_error(self, error):
        self.error_list.append(error)

    def is_document_valid(self):
        return len(self.error_list) == 0


class EDIDocument:
    """
    An EDI X12 Document
    """

    def __init__(self):
        self.text = ""
        self.config = DocumentConfiguration(
            version=DocumentSettings.version,
            element_separator=DocumentSettings.element_separator,
            segment_terminator=DocumentSettings.segment_terminator,
            sub_element_separator=DocumentSettings.sub_element_separator,
        )

        self.interchange = Interchange()

    def format_as_edi(self):
        """Format this document as EDI and return it as a string"""
        return self.interchange.format_as_edi(self.config)

    def validate(self):
        """Validate this document and return a validation report"""
        report = ValidationReport()
        self.interchange.validate(report)
        return report

    def to_dict(self):
        return {
            "document": {
                "text": self.text,
                "config": self.config.to_dict(),
                "interchange": self.interchange.to_dict(),
            }
        }

    def __repr__(self):
        _pp = pp.PrettyPrinter(indent=2)
        return _pp.pformat(self.to_dict())
