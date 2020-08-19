# -*- coding: utf-8 -*-
from typing import List

from badx12.common.helpers import lookahead
from badx12.document.settings import DocumentConfiguration
from badx12.document.validators import ValidationReport

from .segment import GenericHierarchyLevel, GenericNameSegment, Segment


class Envelope(object):
    def __init__(self) -> None:
        self.header: Segment = Segment()
        self.trailer: Segment = Segment()
        self.body: list = []

    def format_as_edi(self, document_configuration: DocumentConfiguration) -> str:
        """
        Format the envelope as an EDI string.
        :param document_configuration: config for formatting.
        :return: document as a string of EDI.
        """
        document: str = self.header.format_as_edi(document_configuration)
        document += self._format_body_as_edi(document_configuration)
        document += self.trailer.format_as_edi(document_configuration)
        return document

    def _format_body_as_edi(self, document_configuration: DocumentConfiguration) -> str:
        """
        Format the body of the envelope as an EDI string.
        This calls format_as_edi in all the children.
        :param document_configuration: config for formatting.
        :return: document as a string of EDI.
        """
        document = ""
        for item in self.body:
            document += item.format_as_edi(document_configuration)
        return document

    def validate(self, report: ValidationReport) -> None:
        """
        Performs validation of the envelope and its components.
        :param report: the validation report to append errors.
        """
        self.header.validate(report)
        self._validate_body(report)
        self.trailer.validate(report)

    def _validate_body(self, report: ValidationReport) -> None:
        """
        Validates each of the children of the envelope.
        :param report: the validation report to append errors.
        """
        for item in self.body:
            item.validate(report)

    def number_of_segments(self) -> int:
        return len(self.body)

    def to_dict(self) -> dict:
        return {
            "header": self.header.to_dict(),
            "trailer": self.trailer.to_dict(),
        }

    def __repr__(self) -> str:
        out = f"{self.__class__.__name__}("
        out += f"header={repr(self.header)}, "

        out += "body=("
        for item, has_more in lookahead(self.body):
            if not issubclass(item.__class__, Envelope):
                out += f"{item.id.name}={repr(item)}"

            else:
                out += f"{item.__class__.__name__}={repr(item)}"

            if has_more:
                out += ", "

        out += "), "
        out += f"trailer={repr(self.trailer)})"

        return out


class InterchangeEnvelope(Envelope):
    def __init__(self) -> None:
        Envelope.__init__(self)
        self.groups: list = self.body


class GroupEnvelope(Envelope):
    def __init__(self) -> None:
        Envelope.__init__(self)
        self.transaction_sets: list = self.body


class TransactionSetEnvelope(Envelope):
    def __init__(self) -> None:
        Envelope.__init__(self)
        self.transaction_body: list = self.body

    def number_of_segments(self) -> int:
        header_trailer_count: int = 2
        return len(self.transaction_body) + header_trailer_count


class GenericLoopEnvelope(Envelope):
    """Generic Loop"""

    def __init__(self) -> None:
        Envelope.__init__(self)
        self.name: GenericNameSegment = GenericNameSegment()
        self.hierarchical_level: GenericHierarchyLevel = GenericHierarchyLevel()
        self.request_validations: list = []
        self.loop_body: list = self.body

    def number_of_segments(self) -> int:
        header_trailer_count: int = 2
        inner_loop_count: int = 0

        for loop in self.loop_body:
            if isinstance(loop, GenericLoopEnvelope):
                inner_loop_count += loop.number_of_segments()

        return len(self.request_validations) + header_trailer_count + inner_loop_count


class InformationSourceLoopEnvelope(GenericLoopEnvelope):
    """Loop 2000A"""

    def __init__(self) -> None:
        GenericLoopEnvelope.__init__(self)
        self.receivers: list = self.body


class InformationReceiverLoopEnvelope(GenericLoopEnvelope):
    """Loop 2000B"""

    def __init__(self) -> None:
        GenericLoopEnvelope.__init__(self)


class SubscriberLoopEnvelope(GenericLoopEnvelope):
    """Loop 2000C"""

    def __init__(self) -> None:
        GenericLoopEnvelope.__init__(self)


class DependentLoopEnvelope(GenericLoopEnvelope):
    """Loop 2000D"""

    def __init__(self) -> None:
        GenericLoopEnvelope.__init__(self)
