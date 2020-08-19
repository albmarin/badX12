# -*- coding: utf-8 -*-
from badx12.document.datastructures import Element, Segment
from badx12.document.datastructures.segment import (
    GenericHierarchyLevel,
    GenericNameSegment,
    GenericRequestValidation,
)


class TransactionSetBHT(Segment):
    """BHT - Beginning of hierarchical transaction"""

    def __init__(self) -> None:
        Segment.__init__(self)
        self.field_count: int = 5

        self.id: Element = Element(
            name="BHT",
            description="Beginning of Hierarchical Transaction",
            required=True,
            min_length=3,
            max_length=3,
            content="BHT",
        )

        self.structure_code: Element = Element(
            name="BHT01",
            description="Hierarchical Structure Code",
            required=True,
            min_length=4,
            max_length=4,
            content="",
        )

        self.purpose_code: Element = Element(
            name="BHT02",
            description="Transaction Set Purpose Code",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )

        self.reference_id: Element = Element(
            name="BHT03",
            description="Reference Identification",
            required=False,
            min_length=1,
            max_length=50,
            content="",
        )

        self.date: Element = Element(
            name="BHT04",
            description="Date",
            required=True,
            min_length=8,
            max_length=8,
            content="",
        )

        self.time: Element = Element(
            name="BHT05",
            description="Time",
            required=True,
            min_length=4,
            max_length=8,
            content="",
        )

        self.bht01: Element = self.structure_code
        self.bht02: Element = self.purpose_code
        self.bht03: Element = self.reference_id
        self.bht04: Element = self.date
        self.bht05: Element = self.time

        self.fields.extend(
            (self.id, self.bht01, self.bht02, self.bht03, self.bht04, self.bht05)
        )

    def to_dict(self) -> dict:
        return {
            "field_count": self.field_count,
            "id": self.id.to_dict(),
            "structure_code": self.structure_code.to_dict(),
            "purpose_code": self.purpose_code.to_dict(),
            "reference_id": self.reference_id.to_dict(),
            "date": self.date.to_dict(),
            "time": self.time.to_dict(),
        }


class InformationSourceName(GenericNameSegment):
    """NM1 - Information Source Name"""

    def __init__(self) -> None:
        GenericNameSegment.__init__(self)

        self.id.description = "Information Source Name"
        self.org_name: Element = self.last_name_or_org_name

    def to_dict(self) -> dict:
        return {
            "field_count": self.field_count,
            "id": self.id.to_dict(),
            "entity_identifier_code": self.entity_identifier_code.to_dict(),
            "entity_type_qualifier": self.entity_type_qualifier.to_dict(),
            "org_name": self.org_name.to_dict(),
            "id_code_qualifier": self.id_code_qualifier.to_dict(),
            "id_code": self.id_code.to_dict(),
        }


class InformationSourceHL(GenericHierarchyLevel):
    """HL - Information Source Level"""

    def __init__(self) -> None:
        GenericHierarchyLevel.__init__(self)


class InformationSourceRequestValidation(GenericRequestValidation):
    """AAA - Request Validation"""

    def __init__(self) -> None:
        GenericRequestValidation.__init__(self)
