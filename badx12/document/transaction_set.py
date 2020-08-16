# -*- coding: utf-8 -*-
from badx12.exceptions import IDMismatchError, SegmentCountError

from .datastructures import Element, Segment, TransactionSetEnvelope
from .validators import ValidationReport


class TransactionSet(TransactionSetEnvelope):
    """An EDI X12 transaction set"""

    def __init__(self) -> None:
        TransactionSetEnvelope.__init__(self)
        self.header: TransactionSetHeader = TransactionSetHeader()
        self.trailer: TransactionSetTrailer = TransactionSetTrailer()

    def validate(self, report: ValidationReport) -> None:
        """
        Validate the envelope
        :param report: the validation report to append errors.
        """
        super(TransactionSetEnvelope, self).validate(report)
        self._validate_control_ids(report)
        self._validate_group_count(report)

    def _validate_control_ids(self, report: ValidationReport) -> None:
        """
        Validate the control id match in the header and trailer
        :param report: the validation report to append errors.
        """
        if self.header.st02.content != self.trailer.se02.content:
            st02_desc: str = self.header.st02.description
            st02_name: str = self.header.st02.name
            se02_desc: str = self.trailer.se02.description
            se02_name: str = self.trailer.se02.name
            report.add_error(
                IDMismatchError(
                    msg=f"The {st02_desc} in {st02_name} does not match {se02_desc} in {se02_name}",
                    segment=self.header.id,
                )
            )

    def _validate_group_count(self, report: ValidationReport) -> None:
        """
        Validate the actual group count matches the specified count.
        :param report: the validation report to append errors.
        """
        if int(self.trailer.se01.content) != self.number_of_segments():
            report.add_error(
                SegmentCountError(
                    msg=f"""The {self.trailer.se01.description} in {self.trailer.se01.name} value of
                    {self.trailer.se01.content} does not match the parsed count of {len(self.transaction_body)}""",
                    segment=self.trailer.id,
                )
            )

    def to_dict(self) -> dict:
        return {
            "header": self.header.to_dict(),
            "trailer": self.trailer.to_dict(),
            "body": [item.to_dict() for item in self.body],
        }


class TransactionSetHeader(Segment):
    """The transaction set header"""

    def __init__(self) -> None:
        Segment.__init__(self)
        self.field_count: int = 3

        self.id: Element = Element(
            name="ST",
            description="Transaction Set Header",
            required=True,
            min_length=2,
            max_length=2,
            content="ST",
        )

        self.identifier_code: Element = Element(
            name="ST01",
            description="Transaction Set Identifier Code",
            required=True,
            min_length=3,
            max_length=3,
            content="",
        )

        self.control_number: Element = Element(
            name="ST02",
            description="Transaction Set Control Number",
            required=True,
            min_length=4,
            max_length=9,
            content="",
        )

        self.implementation_reference: Element = Element(
            name="ST03",
            description="Implementation Convention Reference",
            required=False,
            min_length=1,
            max_length=35,
            content="",
        )

        self.st01: Element = self.identifier_code
        self.st02: Element = self.control_number
        self.st03: Element = self.implementation_reference

        self.fields.extend((self.id, self.st01, self.st02, self.st03))

    def to_dict(self) -> dict:
        return {
            "field_count": self.field_count,
            "id": self.id.to_dict(),
            "identifier_code": self.identifier_code.to_dict(),
            "control_number": self.control_number.to_dict(),
            "implementation_reference": self.implementation_reference.to_dict(),
        }


class TransactionSetTrailer(Segment):
    """The transaction set header"""

    def __init__(self) -> None:
        Segment.__init__(self)
        self.field_count: int = 2

        self.id: Element = Element(
            name="SE",
            description="Transaction Set Trailer",
            required=True,
            min_length=2,
            max_length=2,
            content="SE",
        )

        self.segment_count: Element = Element(
            name="SE01",
            description="Number of Included Segments",
            required=True,
            min_length=1,
            max_length=6,
            content="",
        )

        self.control_number: Element = Element(
            name="SE02",
            description="Transaction Set Control Number",
            required=True,
            min_length=4,
            max_length=9,
            content="",
        )

        self.se01: Element = self.segment_count
        self.se02: Element = self.control_number

        self.fields.extend((self.id, self.se01, self.se02))

    def to_dict(self) -> dict:
        return {
            "field_count": self.field_count,
            "id": self.id.to_dict(),
            "segment_count": self.segment_count.to_dict(),
            "control_number": self.control_number.to_dict(),
        }
