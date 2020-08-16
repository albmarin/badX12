# -*- coding: utf-8 -*-

from badx12.exceptions import IDMismatchError, SegmentCountError

from .datastructures import Element, GroupEnvelope, Segment
from .validators import ValidationReport


class Group(GroupEnvelope):
    """An EDI X12 groups"""

    def __init__(self) -> None:
        GroupEnvelope.__init__(self)
        self.header: GroupHeader = GroupHeader()
        self.trailer: GroupTrailer = GroupTrailer()

    def validate(self, report: ValidationReport) -> None:
        """
        Validate the group envelope
        :param report: the validation report to append errors.
        """
        super(GroupEnvelope, self).validate(report)
        self._validate_control_ids(report)
        self.__validate_group_count(report)

    def _validate_control_ids(self, report: ValidationReport) -> None:
        """
        Validate the control id match in the header and trailer
        :param report: the validation report to append errors.
        """
        if self.header.gs06.content != self.trailer.ge02.content:
            gs06_desc = self.header.gs06.description
            gs06_name = self.header.gs06.name
            ge02_desc = self.trailer.ge02.description
            ge02_name = self.trailer.ge02.name
            report.add_error(
                IDMismatchError(
                    segment=self.header.id,
                    msg=f"The {gs06_desc} in {gs06_name} does not match {ge02_desc} in {ge02_name}",
                )
            )

    def __validate_group_count(self, report: ValidationReport) -> None:
        """
        Validate the actual group count matches the specified count.
        :param report: the validation report to append errors.
        """
        if int(self.trailer.ge01.content) != len(self.transaction_sets):
            report.add_error(
                SegmentCountError(
                    segment=self.trailer.id,
                    msg=f"""The {self.trailer.ge01.description} in {self.trailer.ge01.name} value of
                    {self.trailer.ge01.content}  does not match the parsed count of
                    {str(len(self.transaction_sets))}""",
                )
            )

    def to_dict(self) -> dict:
        return {
            "header": self.header.to_dict(),
            "trailer": self.trailer.to_dict(),
            "transaction_sets": [item.to_dict() for item in self.transaction_sets],
        }


class GroupHeader(Segment):
    """An EDI X12 groups header"""

    def __init__(self) -> None:
        Segment.__init__(self)
        self.field_count: int = 8

        self.id: Element = Element(
            name="GS",
            description="Functional Group Header Code",
            required=True,
            min_length=2,
            max_length=2,
            content="GS",
        )

        self.identifier_code: Element = Element(
            name="GS01",
            description="Functional Identifier Code",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )

        self.sender_code: Element = Element(
            name="GS02",
            description="Application Sender's Code",
            required=True,
            min_length=2,
            max_length=15,
            content="",
        )

        self.receiver_code: Element = Element(
            name="GS03",
            description="Application Receiver's Code",
            required=True,
            min_length=2,
            max_length=15,
            content="",
        )

        self.date: Element = Element(
            name="GS04",
            description="Group Date",
            required=True,
            min_length=8,
            max_length=8,
            content="",
        )

        self.time: Element = Element(
            name="GS05",
            description="Group Time",
            required=True,
            min_length=4,
            max_length=4,
            content="",
        )

        self.control_number: Element = Element(
            name="GS06",
            description="Group Control Number",
            required=True,
            min_length=1,
            max_length=9,
            content="",
        )

        self.agency_code: Element = Element(
            name="GS07",
            description="Responsible Agency Code",
            required=True,
            min_length=1,
            max_length=2,
            content="",
        )

        self.version_code: Element = Element(
            name="GS08",
            description="Version / Release / Industry Identifier Code",
            required=True,
            min_length=1,
            max_length=12,
            content="",
        )

        self.gs01: Element = self.identifier_code
        self.gs02: Element = self.sender_code
        self.gs03: Element = self.receiver_code
        self.gs04: Element = self.date
        self.gs05: Element = self.time
        self.gs06: Element = self.control_number
        self.gs07: Element = self.agency_code
        self.gs08: Element = self.version_code

        self.fields.extend(
            (
                self.id,
                self.gs01,
                self.gs02,
                self.gs03,
                self.gs04,
                self.gs05,
                self.gs06,
                self.gs07,
                self.gs08,
            )
        )

    def to_dict(self) -> dict:
        return {
            "field_count": self.field_count,
            "id": self.id.to_dict(),
            "identifier_code": self.identifier_code.to_dict(),
            "sender_code": self.sender_code.to_dict(),
            "receiver_code": self.receiver_code.to_dict(),
            "date": self.date.to_dict(),
            "time": self.time.to_dict(),
            "control_number": self.time.to_dict(),
            "agency_code": self.agency_code.to_dict(),
            "version_code": self.version_code.to_dict(),
        }


class GroupTrailer(Segment):
    """An EDI X12 groups trailer"""

    def __init__(self) -> None:
        Segment.__init__(self)
        self.field_count: int = 2

        self.id: Element = Element(
            name="GE",
            description="Functional Group Trailer Identifier",
            required=True,
            min_length=2,
            max_length=2,
            content="GE",
        )

        self.transaction_set_count: Element = Element(
            name="GE01",
            description="Number of Transaction Sets Included",
            required=True,
            min_length=1,
            max_length=6,
            content="",
        )

        self.control_number: Element = Element(
            name="GE02",
            description="Group Control Number",
            required=True,
            min_length=1,
            max_length=9,
            content="",
        )

        self.ge01: Element = self.transaction_set_count
        self.ge02: Element = self.control_number

        self.fields.extend((self.id, self.ge01, self.ge02))

    def to_dict(self) -> dict:
        return {
            "field_count": self.field_count,
            "transaction_set_count": self.transaction_set_count.to_dict(),
            "control_number": self.control_number.to_dict(),
        }
