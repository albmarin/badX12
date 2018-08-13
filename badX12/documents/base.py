from badX12.common import Interchange
from badX12.settings import DocumentSettings


class DocumentConfiguration:

    def __init__(self, version, element_separator, segment_terminator, sub_element_separator):
        """Creates a new Edi Document Configuration"""
        self.version = version
        self.element_separator = element_separator
        self.segment_terminator = segment_terminator
        self.sub_element_separator = sub_element_separator


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
        self.configuration = DocumentConfiguration(
            version=DocumentSettings.version,
            element_separator=DocumentSettings.element_separator,
            segment_terminator=DocumentSettings.segment_terminator,
            sub_element_separator=DocumentSettings.sub_element_separator
        )

        self.interchange = Interchange()

    def format_as_edi(self):
        """Format this document as EDI and return it as a string"""
        return self.interchange.format_as_edi(self.document_configuration)

    def validate(self):
        """Validate this document and return a validation report"""
        report = ValidationReport()
        self.interchange.validate(report)
        return report

    def __repr__(self):
        newline = '\n'

        return f"""
        EDIDocument(
            Text => {self.text}
            Document Text => ('{self.document_text}'...)
            Configuration => 
                {self.configuration}
            Interchange => 
                {self.interchange}
            Version => {self.version}
        )    
        """