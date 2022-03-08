# -*- coding: utf-8 -*-
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
        self.big = InterchangeBIG()
        self.ref = InterchangeREF()
        self.n1 = InterchangeN1()
        self.n3 = InterchangeN3()
        self.n4 = InterchangeN4()
        self.txi = InterchangeTXI()
        self.it1 = InterchangeIT1()
        self.sac = InterchangeSAC()

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


class InterchangeBIG(Segment):
    """An EDI X12 interchange BIG"""

    def __init__(self):
        Segment.__init__(self)
        self.field_count = 7

        self.id = Element(
            name="BIG",
            description="Beginning Segment for Invoice",
            required=True,
            min_length=3,
            max_length=3,
            content="",
        )
        self.fields.append(self.id)

        self.big01 = Element(
            name="BIG01",
            description="Invoice Date",
            required=True,
            min_length=8,
            max_length=8,
            content="",
        )
        self.fields.append(self.big01)

        self.big02 = Element(
            name="BIG02",
            description="Invoice Number",
            required=True,
            min_length=1,
            max_length=16,
            content="",
        )
        self.fields.append(self.big02)

        self.big03 = Element(
            name="BIG03",
            description="Purchase Order Date",
            required=True,
            min_length=8,
            max_length=8,
            content="",
        )
        self.fields.append(self.big03)

        self.big04 = Element(
            name="BIG04",
            description="Purchase Order Number",
            required=True,
            min_length=1,
            max_length=10,
            content="",
        )
        self.fields.append(self.big04)

        self.big05 = Element(
            name="BIG05",
            description="Purchase Order Number",
            required=True,
            min_length=1,
            max_length=10,
            content="",
        )
        self.fields.append(self.big05)

        self.big06 = Element(
            name="BIG06",
            description="Purchase Order Number",
            required=True,
            min_length=1,
            max_length=10,
            content="",
        )
        self.fields.append(self.big06)

        self.big07 = Element(
            name="BIG07",
            description="Purchase Order Number",
            required=True,
            min_length=1,
            max_length=10,
            content="",
        )
        self.fields.append(self.big07)

    def to_dict(self):
        return {
            "field_count": self.field_count,
            "fields": [val.to_dict() for val in self.fields],
            "element_separator": self.element_separator,
            "segment_terminator": self.segment_terminator,
            "sub_element_separator": self.sub_element_separator,
        }


class InterchangeREF(Segment):
    """An EDI X12 interchange REF"""

    def __init__(self):
        Segment.__init__(self)
        self.field_count = 2

        self.id = Element(
            name="REF",
            description="Reference Identification",
            required=True,
            min_length=3,
            max_length=3,
            content="",
        )
        self.fields.append(self.id)

        self.ref01 = Element(
            name="REF01",
            description="Reference Identification Qualifier",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.ref01)

        self.ref02 = Element(
            name="REF02",
            description="Reference Identification",
            required=True,
            min_length=10,
            max_length=10,
            content="",
        )
        self.fields.append(self.ref02)

    def to_dict(self):
        return {
            "field_count": self.field_count,
            "fields": [val.to_dict() for val in self.fields],
            "element_separator": self.element_separator,
            "segment_terminator": self.segment_terminator,
            "sub_element_separator": self.sub_element_separator,
        }


class InterchangeN1(Segment):
    """An EDI X12 interchange N1"""

    def __init__(self):
        Segment.__init__(self)
        self.field_count = 4

        self.id = Element(
            name="N1",
            description="Name",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.id)

        self.n101 = Element(
            name="N101",
            description="Entity Identifier Code",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.n101)

        self.n102 = Element(
            name="N102",
            description="Name",
            required=True,
            min_length=1,
            max_length=35,
            content="",
        )
        self.fields.append(self.n102)

        self.n103 = Element(
            name="N103",
            description="Identification Code Qualifier",
            required=False,
            min_length=1,
            max_length=2,
            content="",
        )
        self.fields.append(self.n103)

        self.n104 = Element(
            name="N104",
            description="Identification Code",
            required=False,
            min_length=2,
            max_length=80,
            content="",
        )
        self.fields.append(self.n104)

    def to_dict(self):
        return {
            "field_count": self.field_count,
            "fields": [val.to_dict() for val in self.fields],
            "element_separator": self.element_separator,
            "segment_terminator": self.segment_terminator,
            "sub_element_separator": self.sub_element_separator,
        }


class InterchangeN3(Segment):
    """An EDI X12 interchange N3"""

    def __init__(self):
        Segment.__init__(self)
        self.field_count = 1

        self.id = Element(
            name="N3",
            description="Address Information",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.id)

        self.n301 = Element(
            name="n301",
            description="Address Information",
            required=True,
            min_length=1,
            max_length=20,
            content="",
        )
        self.fields.append(self.n301)

    def to_dict(self):
        return {
            "field_count": self.field_count,
            "fields": [val.to_dict() for val in self.fields],
            "element_separator": self.element_separator,
            "segment_terminator": self.segment_terminator,
            "sub_element_separator": self.sub_element_separator,
        }


class InterchangeN4(Segment):
    """An EDI X12 interchange N4"""

    def __init__(self):
        Segment.__init__(self)
        self.field_count = 6

        self.id = Element(
            name="N4",
            description="Geographic Location",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.id)

        self.n401 = Element(
            name="N401",
            description="City Name",
            required=True,
            min_length=2,
            max_length=30,
            content="",
        )
        self.fields.append(self.n401)

        self.n402 = Element(
            name="N402",
            description="State or Province Code",
            required=True,
            min_length=1,
            max_length=15,
            content="",
        )
        self.fields.append(self.n402)

        self.n403 = Element(
            name="N403",
            description="Postal Code",
            required=True,
            min_length=1,
            max_length=15,
            content="",
        )
        self.fields.append(self.n403)

        self.n404 = Element(
            name="N404",
            description="Country Code",
            required=True,
            min_length=1,
            max_length=3,
            content="",
        )
        self.fields.append(self.n404)

        self.n405 = Element(
            name="N405",
            description="Location Qualifier",
            required=True,
            min_length=1,
            max_length=2,
            content="",
        )
        self.fields.append(self.n405)

        self.n406 = Element(
            name="N406",
            description="Location Identifier",
            required=True,
            min_length=1,
            max_length=15,
            content="",
        )
        self.fields.append(self.n406)

    def to_dict(self):
        return {
            "field_count": self.field_count,
            "fields": [val.to_dict() for val in self.fields],
            "element_separator": self.element_separator,
            "segment_terminator": self.segment_terminator,
            "sub_element_separator": self.sub_element_separator,
        }


class InterchangeIT1(Segment):
    """An EDI X12 interchange IT1"""

    def __init__(self):
        Segment.__init__(self)
        self.field_count = 7

        self.id = Element(
            name="IT1",
            description="Baseline Item Data (Invoice)",
            required=True,
            min_length=3,
            max_length=3,
            content="",
        )
        self.fields.append(self.id)

        self.it101 = Element(
            name="IT101",
            description="Purchase Order Line  Item Number ",
            required=True,
            min_length=1,
            max_length=3,
            content="",
        )
        self.fields.append(self.it101)

        self.it102 = Element(
            name="IT102",
            description="Quantify Invoiced",
            required=True,
            min_length=1,
            max_length=10,
            content="",
        )
        self.fields.append(self.it102)

        self.it103 = Element(
            name="IT103",
            description="Unit or Basis for  Measurement Code",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.it103)

        self.it104 = Element(
            name="IT104",
            description="Unit Price",
            required=True,
            min_length=1,
            max_length=14,
            content="",
        )
        self.fields.append(self.it104)

        self.it105 = Element(
            name="IT105",
            description="Basis of Unit Price Code",
            required=False,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.it105)

        self.it106 = Element(
            name="IT106",
            description="Product / Service ID Qualifier",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.it106)

        self.it107 = Element(
            name="IT107",
            description="Product / Service ID",
            required=True,
            min_length=1,
            max_length=30,
            content="",
        )
        self.fields.append(self.it107)

    def to_dict(self):
        return {
            "field_count": self.field_count,
            "fields": [val.to_dict() for val in self.fields],
            "element_separator": self.element_separator,
            "segment_terminator": self.segment_terminator,
            "sub_element_separator": self.sub_element_separator,
        }


class InterchangeTXI(Segment):
    """An EDI X12 interchange TXI"""

    def __init__(self):
        Segment.__init__(self)
        self.field_count = 3

        self.id = Element(
            name="TXI",
            description="Tax Information",
            required=True,
            min_length=3,
            max_length=3,
            content="",
        )
        self.fields.append(self.id)

        self.txi01 = Element(
            name="TXI01",
            description="Tax Type Code",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.txi01)

        self.txi02 = Element(
            name="TXI02",
            description="Monetary Amount",
            required=True,
            min_length=1,
            max_length=15,
            content="",
        )
        self.fields.append(self.txi02)

        self.txi03 = Element(
            name="TXI03",
            description="Percent",
            required=True,
            min_length=1,
            max_length=10,
            content="",
        )
        self.fields.append(self.txi03)

        self.txi04 = Element(
            name="TXI04",
            description="Unknown",
            required=False,
            min_length=1,
            max_length=100,
            content="",
        )
        self.fields.append(self.txi03)

        self.txi05 = Element(
            name="TXI05",
            description="Unknown",
            required=False,
            min_length=1,
            max_length=100,
            content="",
        )
        self.fields.append(self.txi03)

        self.txi06 = Element(
            name="TXI06",
            description="Unknown",
            required=False,
            min_length=1,
            max_length=100,
            content="",
        )
        self.fields.append(self.txi03)

    def to_dict(self):
        return {
            "field_count": self.field_count,
            "fields": [val.to_dict() for val in self.fields],
            "element_separator": self.element_separator,
            "segment_terminator": self.segment_terminator,
            "sub_element_separator": self.sub_element_separator,
        }


class InterchangeSAC(Segment):
    """An EDI X12 interchange SAC"""

    def __init__(self):
        Segment.__init__(self)
        self.field_count = 16

        self.id = Element(
            name="SAC",
            description="Service, Promotion, Allowance, Charge Information",
            required=True,
            min_length=3,
            max_length=3,
            content="",
        )
        self.fields.append(self.id)

        self.sac01 = Element(
            name="SAC01",
            description="Allowance or Charge Indicator",
            required=True,
            min_length=1,
            max_length=1,
            content="",
        )
        self.fields.append(self.sac01)

        self.sac02 = Element(
            name="SAC02",
            description="Service, Promotion, Allowance, or Charge Code",
            required=True,
            min_length=4,
            max_length=4,
            content="",
        )
        self.fields.append(self.sac02)

        self.sac03 = Element(
            name="SAC03",
            description="Agency Qualifier Code",
            required=False,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.sac03)

        self.sac04 = Element(
            name="SAC04",
            description="Agency Service, Promotion, Allowance, or Charge Code",
            required=False,
            min_length=1,
            max_length=10,
            content="",
        )
        self.fields.append(self.sac04)

        self.sac05 = Element(
            name="SAC05",
            description="Amount",
            required=True,
            min_length=1,
            max_length=15,
            content="",
        )
        self.fields.append(self.sac05)

        self.sac06 = Element(
            name="SAC06",
            description="Allowance/Charge Percent Qualifier",
            required=False,
            min_length=1,
            max_length=1,
            content="",
        )
        self.fields.append(self.sac06)

        self.sac07 = Element(
            name="SAC07",
            description="Percent",
            required=True,
            min_length=1,
            max_length=6,
            content="",
        )
        self.fields.append(self.sac07)

        self.sac08 = Element(
            name="SAC08",
            description="Rate",
            required=True,
            min_length=1,
            max_length=9,
            content="",
        )
        self.fields.append(self.sac08)

        self.sac09 = Element(
            name="SAC09",
            description="Unit or Basis for Measurement Code",
            required=False,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.sac09)

        self.sac10 = Element(
            name="SAC10",
            description="Quantity",
            required=False,
            min_length=1,
            max_length=15,
            content="",
        )
        self.fields.append(self.sac10)

        self.sac11 = Element(
            name="SAC11",
            description="Quantity",
            required=False,
            min_length=1,
            max_length=15,
            content="",
        )
        self.fields.append(self.sac11)

        self.sac12 = Element(
            name="SAC12",
            description="Allowance or Charge Method of Handling Code",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )
        self.fields.append(self.sac12)

        self.sac13 = Element(
            name="SAC13",
            description="Reference Identification",
            required=False,
            min_length=1,
            max_length=30,
            content="",
        )
        self.fields.append(self.sac13)

        self.sac14 = Element(
            name="SAC14",
            description="Option Number",
            required=False,
            min_length=1,
            max_length=20,
            content="",
        )
        self.fields.append(self.sac14)

        self.sac15 = Element(
            name="SAC15",
            description="Description",
            required=False,
            min_length=1,
            max_length=80,
            content="",
        )
        self.fields.append(self.sac15)

        self.sac16 = Element(
            name="SAC16",
            description="Language Code",
            required=False,
            min_length=2,
            max_length=3,
            content="",
        )
        self.fields.append(self.sac16)

    def to_dict(self):
        return {
            "field_count": self.field_count,
            "fields": [val.to_dict() for val in self.fields],
            "element_separator": self.element_separator,
            "segment_terminator": self.segment_terminator,
            "sub_element_separator": self.sub_element_separator,
        }
