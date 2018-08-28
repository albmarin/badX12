from badX12.settings import DocumentSettings
from .element import Element


class Segment(object):
    def __init__(self):
        self.fieldCount = 0
        self.fields = []
        self.id = Element()
        self.element_separator = DocumentSettings.element_separator
        self.segment_terminator = DocumentSettings.segment_terminator
        self.sub_element_separator = DocumentSettings.sub_element_separator

    def validate(self, report):
        """
        Validate the segment by validating all elements.
        :param report: the validation report to append errors.
        """
        for field in self.fields:
            field.validate(report)

    def format_as_edi(self, document_configuration):
        """Format the segment into an EDI string"""
        self.element_separator = document_configuration.element_separator
        self.segment_terminator = document_configuration.segment_terminator
        self.sub_element_separator = document_configuration.sub_element_separator
        return str(self)

    def __str__(self):
        """Return the segment as a string"""
        out = ""
        if self.__all_fields_empty():
            return out
        out = self.__get_fields_as_string(out)
        return out

    def __all_fields_empty(self):
        """determine if all fields are empty"""
        for field in self.fields:
            if field.content != "":
                return False
        return True

    def __get_fields_as_string(self, out):
        """processes all the fields in the segment and returns the string representation"""
        for index, field in enumerate(self.fields):
            if field.content:
                out += str(field)
                out = self.__add_separators_to_fields(index, out)
        out = self.__add_segment_terminator(out)

        return out

    def __add_separators_to_fields(self, index, out):
        """adds field separators to all the element strings"""
        if index < self.fieldCount:
            # if the next field is required add the separator
            if self.fields[index + 1].required:
                out += self.element_separator
            # if the next field is optional but has content add the separator
            elif self.fields[index + 1].content:
                out += self.element_separator
            # finally if the next field is not the last element add the separator
            elif index + 1 != self.fieldCount:
                out += self.element_separator
        return out

    def __add_segment_terminator(self, out):
        """Adds the segment terminator to the segment string"""
        out += self.segment_terminator
        return out

    def __repr__(self):
        return f"""
            Segment(
                Field Count => {self.fieldCount}
                Fields => {self.fields}
                Element Separator => {self.element_separator}
                Segment Terminator => {self.segment_terminator}
                Sub Element Separator => {self.sub_element_separator}
            )
        """