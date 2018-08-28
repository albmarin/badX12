from badX12.common import InterchangeHeader, Element, Segment
from badX12.common.errors import InvalidFileTypeError, SegmentTerminatorNotFoundError
from badX12.documents import EDIDocument
from ._group import Group, GroupHeader, GroupTrailer
from ._transaction_set import TransactionSet, TransactionSetHeader, TransactionSetTrailer
import os

class Parser:
    def __init__(self):
        """Create a new Parser"""
        self.edi_document = EDIDocument()
        self.document_text = ""

    def parse_document(self, document_text):
        """Parse the text document into an object
        :param document_text:  the text to parse into an EDI document.
        """
        if os.path.isfile(document_text):
            with open(document_text, 'r') as x12File:
                document_text = x12File.read().strip()

        self.document_text = document_text.replace('\n', '').strip()
        # attach the original document text to the document.
        self.edi_document.document_text = self.document_text

        if self.document_text.startswith(EDIDocument().interchange.header.id.name):
            self.__parse_interchange_header()
            self.__separate_and_route_segments()

        else:
            found_segment = self.document_text[:3]
            raise InvalidFileTypeError(segment=found_segment,
                                       msg="Expected Element Envelope: " + EDIDocument().interchange.header.id.name +
                                           " but found Element Envelope: " + found_segment +
                                           ".\n The length of the expected segment is: " + str(
                                           len(EDIDocument().interchange.header.id.name)) +
                                           " the length of the segment found was: " + str(len(found_segment)))

        return self.edi_document

    def __parse_interchange_header(self):
        """Parse the interchange header segment"""
        header = self.edi_document.interchange.header
        # The edi separator is always at position 4
        self.edi_document.configuration.element_separator = self.document_text[3:4]
        header_field_list = self.document_text.split(self.edi_document.configuration.element_separator)
        for index, isa in enumerate(header_field_list):
            if index == 12:
                self.edi_document.version = isa
            if index <= 15:
                header.fields[index].content = isa
            if index == 16:
                last_header_field = header_field_list[16]
                # the sub-element separator is always the first character in this element.
                header.isa16.content = last_header_field[0:1]
                if last_header_field[1:2]:
                    self.edi_document.configuration.segment_terminator = last_header_field[1:2]
                else:
                    raise SegmentTerminatorNotFoundError(
                        msg="The segment terminator is not present in the Interchange Header, can't parse file.")

    def __separate_and_route_segments(self):
        """Handles separating all the segments"""
        self.segment_list = self.document_text.split(self.edi_document.configuration.segment_terminator)
        for segment in self.segment_list:
            self.__route_segment_to_parser(segment)

    def __route_segment_to_parser(self, segment):
        """Take a generic segment and determine what segment to parse it as
        :param segment:
        """
        if segment.startswith(InterchangeHeader().id.name):
            pass
        elif segment.startswith(GroupHeader().id.name):
            self.__parse_group_header(segment)
        elif segment.startswith(GroupTrailer().id.name):
            self.__parse_group_trailer(segment)
        elif segment.startswith(TransactionSetHeader().id.name):
            self.__parse_transaction_set_header(segment)
        elif segment.startswith(TransactionSetTrailer().id.name):
            self.__parse_transaction_set_trailer(segment)
        elif segment.startswith(EDIDocument().interchange.trailer.id.name):
            self.__parse_interchange_trailer(segment)
        else:
            self.__parse_unknown_body(segment)

    def __parse_segment(self, segment, segment_field_list):
        """Generically parse segments
        :param segment: the segment to insert the values.
        :param segment_field_list: the list of segments to parse.
        """
        for index, value in enumerate(segment_field_list):
            segment.fields[index].content = value

    def __create_generic_element(self, index, value):
        """
        Create a generic element based on the data found. Populate all the
        fields so that validation will pass.
        :param index: the position of the element for providing a name.
        :param value: the content for the element being created.
        :return: a generic element.
        """
        element = Element()
        element.name = "GEN" + str(index)
        element.content = value
        element.description = "A generic element created by the parser"
        element.required = False
        length = len(value)
        element.minLength = length
        element.maxLength = length
        return element

    def __parse__unknown_segment(self, segment, segmentFieldList):
        """Generically parse unknown segments by creating a
        new element and appending it to the segment.
        :param segment: the segment to append the values.
        :param segmentFieldList: the list of segments to parse.
        """
        for index, value in enumerate(segmentFieldList):
            element = self.__create_generic_element(index, value)
            segment.fields.append(element)

    def __parse_group_header(self, segment):
        """Parse the group header"""
        self.current_group = Group()
        header = GroupHeader()
        header_field_list = segment.split(self.edi_document.configuration.element_separator)
        self.__parse_segment(header, header_field_list)
        self.current_group.header = header

    def __parse_group_trailer(self, segment):
        """Parse the group trailer"""
        trailer = GroupTrailer()
        trailer_field_list = segment.split(self.edi_document.configuration.element_separator)
        self.__parse_segment(trailer, trailer_field_list)
        self.current_group.trailer = trailer
        self.edi_document.interchange.groups.append(self.current_group)

    def __parse_interchange_trailer(self, segment):
        """Parse the interchange trailer segment"""
        trailer = self.edi_document.interchange.trailer
        trailer_field_list = segment.split(self.edi_document.configuration.element_separator)
        self.__parse_segment(trailer, trailer_field_list)

    def __parse_transaction_set_header(self, segment):
        """Parse transaction set header
        Creates a new transaction set and set it as the current transaction set.
        """
        self.current_transaction = TransactionSet()
        transaction_header = TransactionSetHeader()
        header_field_list = segment.split(self.edi_document.configuration.element_separator)
        self.__parse_segment(transaction_header, header_field_list)
        self.current_transaction.header = transaction_header

    def __parse_transaction_set_trailer(self, segment):
        """Parse the transaction set trailer.
        Adds the completed transaction to a edi document.
        """
        transaction_trailer = TransactionSetTrailer()
        trailer_field_list = segment.split(self.edi_document.configuration.element_separator)
        self.__parse_segment(transaction_trailer, trailer_field_list)
        self.current_transaction.trailer = transaction_trailer
        self.current_group.transaction_sets.append(self.current_transaction)

    def __parse_unknown_body(self, segment):
        if segment:
            generic_segment = Segment()
            generic_field_list = segment.split(self.edi_document.configuration.element_separator)
            self.__parse__unknown_segment(generic_segment, generic_field_list)
            try:
                self.current_transaction.transaction_body.append(generic_segment)
            except AttributeError:
                pass
