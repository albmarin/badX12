# -*- coding: utf-8 -*-

from badx12.document import Element, GroupEnvelope, Segment
from badx12.document.errors import IDMismatchError, SegmentCountError

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
            "body": [item.to_dict() for item in self.body],
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
        self.fields.append(self.id)

        self.gs01: Element = Element(
            name="GS01",
            description="Functional Identifier Code",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.gs01)

        self.gs02: Element = Element(
            name="GS02",
            description="Application Senders Code",
            required=True,
            min_length=2,
            max_length=15,
            content="",
        )
        self.fields.append(self.gs02)

        self.gs03: Element = Element(
            name="GS03",
            description="Application Receiver Code",
            required=True,
            min_length=2,
            max_length=15,
            content="",
        )
        self.fields.append(self.gs03)

        self.gs04: Element = Element(
            name="GS04",
            description="Group Date",
            required=True,
            min_length=8,
            max_length=8,
            content="",
        )
        self.fields.append(self.gs04)

        self.gs05: Element = Element(
            name="GS05",
            description="Group Time",
            required=True,
            min_length=4,
            max_length=4,
            content="",
        )
        self.fields.append(self.gs05)

        self.gs06: Element = Element(
            name="GS06",
            description="Group Control Number",
            required=True,
            min_length=1,
            max_length=9,
            content="",
        )
        self.fields.append(self.gs06)

        self.gs07: Element = Element(
            name="GS07",
            description="Responsible Agency Code",
            required=True,
            min_length=1,
            max_length=2,
            content="",
        )
        self.fields.append(self.gs07)

        self.gs08: Element = Element(
            name="GS08",
            description="Version Indicator ID Code",
            required=True,
            min_length=1,
            max_length=12,
            content="",
        )
        self.fields.append(self.gs08)

    def to_dict(self) -> dict:
        return {
            "field_count": self.field_count,
            "fields": [field.to_dict() for field in self.fields],
            "element_separator": self.element_separator,
            "segment_terminator": self.segment_terminator,
            "sub_element_separator": self.sub_element_separator,
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
        self.fields.append(self.id)

        self.ge01: Element = Element(
            name="GE01",
            description="Number of Transaction Sets",
            required=True,
            min_length=1,
            max_length=6,
            content="",
        )
        self.fields.append(self.ge01)

        self.ge02: Element = Element(
            name="GE02",
            description="Group Control Number",
            required=True,
            min_length=1,
            max_length=9,
            content="",
        )
        self.fields.append(self.ge02)

    def to_dict(self) -> dict:
        return {
            "field_count": self.field_count,
            "fields": [field.to_dict() for field in self.fields],
            "element_separator": self.element_separator,
            "segment_terminator": self.segment_terminator,
            "sub_element_separator": self.sub_element_separator,
        }
