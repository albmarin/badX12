# -*- coding: utf-8 -*-
from .element import Element
from .envelope import InterchangeEnvelope
from .errors import IDMismatchError, SegmentCountError
from .segment import Segment
from .validators import ValidationReport


class Interchange(InterchangeEnvelope):
    """An EDI X12 interchange"""

    def __init__(self) -> None:
        InterchangeEnvelope.__init__(self)
        self.header: InterchangeHeader = InterchangeHeader()
        self.trailer: InterchangeTrailer = InterchangeTrailer()

    def validate(self, report: ValidationReport) -> None:
        """
        Validate the envelope
        :param report: the validation report to append errors.
        """
        super(InterchangeEnvelope, self).validate(report)
        self._validate_control_ids(report)
        self._validate_group_count(report)

    def _validate_control_ids(self, report: ValidationReport) -> None:
        """
        Validate the control id match in the header and trailer
        :param report: the validation report to append errors.
        """
        if self.header.isa13.content != self.trailer.iea02.content:
            isa13_desc: str = self.header.isa13.description
            isa13_name: str = self.header.isa13.name
            iea02_desc: str = self.trailer.iea02.description
            iea02_name: str = self.trailer.iea02.name
            report.add_error(
                IDMismatchError(
                    msg=f"The {isa13_desc}  in {isa13_name} does not match {iea02_desc} in {iea02_name}",
                    segment=self.header.id,
                )
            )

    def _validate_group_count(self, report: ValidationReport) -> None:
        """
        Validate the actual group count matches the specified count.
        :param report: the validation report to append errors.
        """
        if int(self.trailer.iea01.content) != len(self.groups):
            report.add_error(
                SegmentCountError(
                    msg=f"""The {self.trailer.iea01.description} in {self.trailer.iea01.name} value of
                    {self.trailer.iea01.content} does not match the parsed count of {len(self.groups)}""",
                    segment=self.trailer.id,
                )
            )

    def to_dict(self) -> dict:
        return {
            "header": self.header.to_dict(),
            "trailer": self.trailer.to_dict(),
            "groups": [group.to_dict() for group in self.groups],
        }


class InterchangeHeader(Segment):
    """An EDI X12 interchange header"""

    def __init__(self) -> None:
        Segment.__init__(self)
        self.field_count: int = 16

        self.id: Element = Element(
            name="ISA",
            description="Interchange Control Header Code",
            required=True,
            min_length=3,
            max_length=3,
            content="ISA",
        )

        self.authorization_info_qualifier: Element = Element(
            name="ISA01",
            description="Authorization Information Qualifier",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )

        self.authorization_info: Element = Element(
            name="ISA02",
            description="Authorization Information",
            required=True,
            min_length=10,
            max_length=10,
            content="",
        )

        self.security_info_qualifier: Element = Element(
            name="ISA03",
            description="Security Information Qualifier",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )

        self.security_info: Element = Element(
            name="ISA04",
            description="Security Information",
            required=True,
            min_length=10,
            max_length=10,
            content="",
        )

        self.sender_id_qualifier: Element = Element(
            name="ISA05",
            description="Interchange ID Qualifier",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )

        self.sender_id = Element(
            name="ISA06",
            description="Interchange Sender ID",
            required=True,
            min_length=15,
            max_length=15,
            content="",
        )

        self.receiver_id_qualifier: Element = Element(
            name="ISA07",
            description="Interchange ID Qualifier",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )

        self.receiver_id: Element = Element(
            name="ISA08",
            description="Interchange Receiver ID",
            required=True,
            min_length=15,
            max_length=15,
            content="",
        )

        self.date: Element = Element(
            name="ISA09",
            description="Interchange Date",
            required=True,
            min_length=6,
            max_length=6,
            content="",
        )

        self.time: Element = Element(
            name="ISA10",
            description="Interchange Time",
            required=True,
            min_length=4,
            max_length=4,
            content="",
        )

        self.repetition_separator: Element = Element(
            name="ISA11",
            description="Repetition Separator",
            required=True,
            min_length=1,
            max_length=1,
            content="",
        )

        self.control_version: Element = Element(
            name="ISA12",
            description="Interchange Control Version Number",
            required=True,
            min_length=5,
            max_length=5,
            content="",
        )

        self.control_number: Element = Element(
            name="ISA13",
            description="Interchange Control Number",
            required=True,
            min_length=9,
            max_length=9,
            content="",
        )

        self.acknowledgement_requested: Element = Element(
            name="ISA14",
            description="Acknowledgement Requested",
            required=True,
            min_length=1,
            max_length=1,
            content="",
        )

        self.usage_indicator: Element = Element(
            name="ISA15",
            description="Interchange Usage Indicator",
            required=True,
            min_length=1,
            max_length=1,
            content="",
        )

        self.component_element_separator: Element = Element(
            name="ISA16",
            description="Component Element Separator",
            required=True,
            min_length=1,
            max_length=1,
            content="",
        )

        self.isa01: Element = self.authorization_info_qualifier
        self.isa02: Element = self.authorization_info
        self.isa03: Element = self.security_info_qualifier
        self.isa04: Element = self.security_info
        self.isa05: Element = self.sender_id_qualifier
        self.isa06: Element = self.sender_id
        self.isa07: Element = self.receiver_id_qualifier
        self.isa08: Element = self.receiver_id
        self.isa09: Element = self.date
        self.isa10: Element = self.time
        self.isa11: Element = self.repetition_separator
        self.isa12: Element = self.control_version
        self.isa13: Element = self.control_number
        self.isa14: Element = self.acknowledgement_requested
        self.isa15: Element = self.usage_indicator
        self.isa16: Element = self.component_element_separator

        self.fields.extend(
            (
                self.id,
                self.isa01,
                self.isa02,
                self.isa03,
                self.isa04,
                self.isa05,
                self.isa06,
                self.isa07,
                self.isa08,
                self.isa09,
                self.isa10,
                self.isa11,
                self.isa12,
                self.isa13,
                self.isa14,
                self.isa15,
                self.isa16,
            )
        )

    def to_dict(self) -> dict:
        return {
            "field_count": self.field_count,
            "id": self.id.to_dict(),
            "authorization_info_qualifier": self.authorization_info_qualifier.to_dict(),
            "authorization_info": self.authorization_info.to_dict(),
            "security_info_qualifier": self.security_info_qualifier.to_dict(),
            "security_info": self.security_info.to_dict(),
            "sender_id_qualifier": self.sender_id_qualifier.to_dict(),
            "sender_id": self.sender_id.to_dict(),
            "receiver_id_qualifier": self.receiver_id_qualifier.to_dict(),
            "receiver_id": self.receiver_id.to_dict(),
            "date": self.date.to_dict(),
            "time": self.time.to_dict(),
            "repetition_separator": self.repetition_separator.to_dict(),
            "control_version": self.control_version.to_dict(),
            "control_number": self.control_number.to_dict(),
            "acknowledgement_requested": self.acknowledgement_requested.to_dict(),
            "usage_indicator": self.usage_indicator.to_dict(),
            "component_element_separator": self.component_element_separator.to_dict(),
        }


class InterchangeTrailer(Segment):
    """An EDI X12 interchange Trailer"""

    def __init__(self) -> None:
        Segment.__init__(self)
        self.field_count: int = 2

        self.id: Element = Element(
            name="IEA",
            description="Interchange Control Trailer Code",
            required=True,
            min_length=3,
            max_length=3,
            content="",
        )

        self.group_count: Element = Element(
            name="IEA01",
            description="Number of Included Functional Groups",
            required=True,
            min_length=1,
            max_length=5,
            content="",
        )

        self.control_number: Element = Element(
            name="IEA02",
            description="Interchange Control Number",
            required=True,
            min_length=1,
            max_length=9,
            content="",
        )

        self.iea01: Element = self.group_count
        self.iea02: Element = self.control_number

        self.fields.extend((self.id, self.iea01, self.iea02))

    def to_dict(self) -> dict:
        return {
            "field_count": self.field_count,
            "id": self.id.to_dict(),
            "group_count": self.group_count.to_dict(),
            "control_number": self.control_number.to_dict(),
        }
