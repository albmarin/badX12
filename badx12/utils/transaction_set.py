import pprint as pp

from badx12.utils import TransactionSetEnvelope, Element, Segment
from badx12.utils.errors import IDMismatchError, SegmentCountError


class TransactionSet(TransactionSetEnvelope):
    """An EDI X12 transaction set"""

    def __init__(self):
        TransactionSetEnvelope.__init__(self)
        self.header = TransactionSetHeader()
        self.trailer = TransactionSetTrailer()

    def validate(self, report):
        """
        Validate the envelope
        :param report: the validation report to append errors.
        """
        super(TransactionSetEnvelope, self).validate(report)
        self._validate_control_ids(report)
        self._validate_group_count(report)

    def _validate_control_ids(self, report):
        """
        Validate the control id match in the header and trailer
        :param report: the validation report to append errors.
        """
        if self.header.st02.content != self.trailer.se02.content:
            st02_desc = self.header.st02.description
            st02_name = self.header.st02.name
            se02_desc = self.trailer.se02.description
            se02_name = self.trailer.se02.name
            report.add_error(
                IDMismatchError(
                    msg="The "
                    + st02_desc
                    + " in "
                    + st02_name
                    + " does not match "
                    + se02_desc
                    + " in "
                    + se02_name,
                    segment=self.header.id,
                )
            )

    def _validate_group_count(self, report):
        """
        Validate the actual group count matches the specified count.
        :param report: the validation report to append errors.
        """
        if int(self.trailer.se01.content) != self.number_of_segments():
            report.add_error(
                SegmentCountError(
                    msg=f"The {self.trailer.se01.description} in {self.trailer.se01.name} value of "
                    f"{self.trailer.se01.content} does not match the parsed count of {len(self.transaction_body)}",
                    segment=self.trailer.id,
                )
            )

    def to_dict(self):
        return {
            "transaction_set": {
                "header": self.header,
                "trailer": self.trailer,
                "body": self.body,
            }
        }

    def __repr__(self):
        _pp = pp.PrettyPrinter()
        return _pp.pformat(self.to_dict())


class TransactionSetHeader(Segment):
    """The transaction set header"""

    def __init__(self):
        Segment.__init__(self)
        self.fieldCount = 3

        self.id = Element(
            name="ST",
            description="Transaction Set Header",
            required=True,
            min_length=2,
            max_length=2,
            content="ST",
        )
        self.fields.append(self.id)

        self.st01 = Element(
            name="ST01",
            description="Transaction Set ID Code",
            required=True,
            min_length=3,
            max_length=3,
            content="",
        )
        self.fields.append(self.st01)

        self.st02 = Element(
            name="ST02",
            description="Transaction Set Control Number",
            required=True,
            min_length=4,
            max_length=9,
            content="",
        )
        self.fields.append(self.st02)

        self.st03 = Element(
            name="ST03",
            description="Implementation Convention Reference",
            required=False,
            min_length=1,
            max_length=35,
            content="",
        )
        self.fields.append(self.st03)

    def to_dict(self):
        return {
            "transaction_set_header": {
                "field_count": self.field_count,
                "fields": self.fields,
            }
        }

    def __repr__(self):
        _pp = pp.PrettyPrinter()
        return _pp.pformat(self.to_dict())


class TransactionSetTrailer(Segment):
    """The transaction set header"""

    def __init__(self):
        Segment.__init__(self)
        self.fieldCount = 2

        self.id = Element(
            name="SE",
            description="Transaction Set Trailer",
            required=True,
            min_length=2,
            max_length=2,
            content="SE",
        )
        self.fields.append(self.id)

        self.se01 = Element(
            name="SE01",
            description="Number of Included Segments",
            required=True,
            min_length=1,
            max_length=6,
            content="",
        )
        self.fields.append(self.se01)

        self.se02 = Element(
            name="SE02",
            description="Transaction Set Control Number",
            required=True,
            min_length=4,
            max_length=9,
            content="",
        )
        self.fields.append(self.se02)
