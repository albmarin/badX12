import pprint as pp

from .element import Element
from .envelope import InterchangeEnvelope
from .errors import IDMismatchError, SegmentCountError
from .segment import Segment


class Interchange(InterchangeEnvelope):
    """An EDI X12 interchange"""

    def __init__(self):
        InterchangeEnvelope.__init__(self)
        self.header = InterchangeHeader()
        self.trailer = InterchangeTrailer()

    def validate(self, report):
        """
        Validate the envelope
        :param report: the validation report to append errors.
        """
        super(InterchangeEnvelope, self).validate(report)
        self._validate_control_ids(report)
        self._validate_group_count(report)

    def _validate_control_ids(self, report):
        """
        Validate the control id match in the header and trailer
        :param report: the validation report to append errors.
        """
        if self.header.isa13.content != self.trailer.iea02.content:
            isa13_desc = self.header.isa13.description
            isa13_name = self.header.isa13.name
            iea02_desc = self.trailer.iea02.description
            iea02_name = self.trailer.iea02.name
            report.add_error(
                IDMismatchError(
                    msg=f"The {isa13_desc}  in {isa13_name} does not match {iea02_desc} in {iea02_name}",
                    segment=self.header.id,
                )
            )

    def _validate_group_count(self, report):
        """
        Validate the actual group count matches the specified count.
        :param report: the validation report to append errors.
        """
        if int(self.trailer.iea01.content) != len(self.groups):
            report.add_error(
                SegmentCountError(
                    msg=f"The {self.trailer.iea01.description} in {self.trailer.iea01.name} value of "
                    f"{self.trailer.iea01.content} does not match the parsed count of {len(self.groups)}",
                    segment=self.trailer.id,
                )
            )

    def to_dict(self):
        return {
            "header": self.header.to_dict(),
            "trailer": self.trailer.to_dict(),
            "body": [item.to_dict() for item in self.body],
            "groups": [group.to_dict() for group in self.groups],
        }


class InterchangeHeader(Segment):
    """An EDI X12 interchange header"""

    def __init__(self):
        Segment.__init__(self)
        self.field_count = 16

        self.id = Element(
            name="ISA",
            description="Interchange Control Header Code",
            required=True,
            min_length=3,
            max_length=3,
            content="ISA",
        )
        self.fields.append(self.id)

        self.isa01 = Element(
            name="ISA01",
            description="Authorization Information Qualifier",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.isa01)

        self.isa02 = Element(
            name="ISA02",
            description="Authorization Information",
            required=True,
            min_length=10,
            max_length=10,
            content="",
        )
        self.fields.append(self.isa02)

        self.isa03 = Element(
            name="ISA03",
            description="Security Information Qualifier",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.isa03)

        self.isa04 = Element(
            name="ISA04",
            description="Security Information",
            required=True,
            min_length=10,
            max_length=10,
            content="",
        )
        self.fields.append(self.isa04)

        self.isa05 = Element(
            name="ISA05",
            description="Interchange ID Qualifier",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.isa05)

        self.isa06 = Element(
            name="ISA06",
            description="Interchange Sender ID",
            required=True,
            min_length=15,
            max_length=15,
            content="",
        )
        self.fields.append(self.isa06)

        self.isa07 = Element(
            name="ISA07",
            description="Interchange ID Qualifier",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.isa07)

        self.isa08 = Element(
            name="ISA08",
            description="Interchange Receiver ID",
            required=True,
            min_length=15,
            max_length=15,
            content="",
        )
        self.fields.append(self.isa08)

        self.isa09 = Element(
            name="ISA09",
            description="Interchange Date",
            required=True,
            min_length=6,
            max_length=6,
            content="",
        )
        self.fields.append(self.isa09)

        self.isa10 = Element(
            name="ISA10",
            description="Interchange Time",
            required=True,
            min_length=4,
            max_length=4,
            content="",
        )
        self.fields.append(self.isa10)

        self.isa11 = Element(
            name="ISA11",
            description="Interchange Control Standard ID",
            required=True,
            min_length=1,
            max_length=1,
            content="",
        )
        self.fields.append(self.isa11)

        self.isa12 = Element(
            name="ISA12",
            description="Interchange Control Version Number",
            required=True,
            min_length=5,
            max_length=5,
            content="",
        )
        self.fields.append(self.isa12)

        self.isa13 = Element(
            name="ISA13",
            description="Interchange Control Number",
            required=True,
            min_length=9,
            max_length=9,
            content="",
        )
        self.fields.append(self.isa13)

        self.isa14 = Element(
            name="ISA14",
            description="Acknowledgement Requested Flag",
            required=True,
            min_length=1,
            max_length=1,
            content="",
        )
        self.fields.append(self.isa14)

        self.isa15 = Element(
            name="ISA15",
            description="Test Indicator",
            required=True,
            min_length=1,
            max_length=1,
            content="",
        )
        self.fields.append(self.isa15)

        self.isa16 = Element(
            name="ISA16",
            description="Sub-element Separator",
            required=True,
            min_length=1,
            max_length=1,
            content="",
        )
        self.fields.append(self.isa16)

    def to_dict(self):
        return {
            "field_count": self.field_count,
            "fields": [val.to_dict() for val in self.fields],
            "element_separator": self.element_separator,
            "segment_terminator": self.segment_terminator,
            "sub_element_separator": self.sub_element_separator,
        }


class InterchangeTrailer(Segment):
    """An EDI X12 interchange Trailer"""

    def __init__(self):
        Segment.__init__(self)
        self.field_count = 2

        self.id = Element(
            name="IEA",
            description="Interchange Control Trailer Code",
            required=True,
            min_length=3,
            max_length=3,
            content="",
        )
        self.fields.append(self.id)

        self.iea01 = Element(
            name="IEA01",
            description="Number of Included Groups",
            required=True,
            min_length=1,
            max_length=5,
            content="",
        )
        self.fields.append(self.iea01)

        self.iea02 = Element(
            name="IEA02",
            description="Interchange Control Number",
            required=True,
            min_length=1,
            max_length=9,
            content="",
        )
        self.fields.append(self.iea02)

    def to_dict(self):
        return {
            "field_count": self.field_count,
            "fields": [val.to_dict() for val in self.fields],
            "element_separator": self.element_separator,
            "segment_terminator": self.segment_terminator,
            "sub_element_separator": self.sub_element_separator,
        }
