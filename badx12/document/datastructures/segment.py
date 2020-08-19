# -*- coding: utf-8 -*-
from typing import List

from badx12.common.helpers import lookahead
from badx12.document.settings import DocumentConfiguration, DocumentSettings
from badx12.document.validators import ValidationReport

from .element import Element


class Segment(object):
    def __init__(self) -> None:
        self.field_count: int = 0
        self.fields: List[Element] = []
        self.id: Element = Element()
        self.element_separator: str = DocumentSettings.element_separator
        self.segment_terminator: str = DocumentSettings.segment_terminator
        self.sub_element_separator: str = DocumentSettings.sub_element_separator

    def validate(self, report: ValidationReport) -> None:
        """
        Validate the segment by validating all elements.
        :param report: the validation report to append errors.
        """
        for field in self.fields:
            field.validate(report)

    def format_as_edi(self, document_configuration: DocumentConfiguration) -> str:
        """Format the segment into an EDI string"""
        self.element_separator = document_configuration.element_separator
        self.segment_terminator = document_configuration.segment_terminator
        self.sub_element_separator = document_configuration.sub_element_separator
        return str(self)

    def _all_fields_empty(self) -> bool:
        """determine if all fields are empty"""
        for field in self.fields:
            if field.content != "":
                return False
        return True

    def _get_fields_as_string(self, out: str) -> str:
        """processes all the fields in the segment and returns the string representation"""
        for index, field in enumerate(self.fields):
            out += str(field)
            out = self._add_separators_to_fields(index, out)
        out = self._add_segment_terminator(out)

        return out

    def _add_separators_to_fields(self, index: int, out: str) -> str:
        """adds field separators to all the element strings"""
        if index < self.field_count:
            # if the next field is required add the separator
            if self.fields[index + 1].required:
                out += self.element_separator
            # if the next field is optional but has content add the separator
            elif self.fields[index + 1].content:
                out += self.element_separator
            # finally if the next field is not the last element add the separator
            elif index + 1 != self.field_count:
                out += self.element_separator
        return out

    def _add_segment_terminator(self, out: str) -> str:
        """Adds the segment terminator to the segment string"""
        out += self.segment_terminator
        return out

    def to_dict(self) -> dict:
        return {
            "field_count": self.field_count,
            "id": self.id.to_dict(),
            **{field.name: field.to_dict() for field in self.fields[1:]},
        }

    def __str__(self) -> str:
        """Return the segment as a string"""
        out: str = ""
        if self._all_fields_empty():
            return out
        out = self._get_fields_as_string(out)
        return out

    def __repr__(self) -> str:
        out = f"{self.__class__.__name__}("
        for field, has_more in lookahead(self.fields):
            out += f"{field.name}={repr(field)}"
            if has_more:
                out += ", "

        out += ")"
        return out


class GenericNameSegment(Segment):
    """NM1 - Generic Name"""

    def __init__(self) -> None:
        Segment.__init__(self)
        self.field_count: int = 12

        self.id: Element = Element(
            name="NM1",
            description="Generic Name",
            required=True,
            min_length=3,
            max_length=3,
            content="NM1",
        )

        self.entity_identifier_code: Element = Element(
            name="NM101",
            description="Entity Identifier Code",
            required=True,
            min_length=2,
            max_length=3,
            content="",
        )

        self.entity_type_qualifier: Element = Element(
            name="NM102",
            description="Entity Type Qualifier",
            required=True,
            min_length=1,
            max_length=1,
            content="",
        )

        self.last_name_or_org_name: Element = Element(
            name="NM103",
            description="Name Last or Organization Name",
            required=True,
            min_length=1,
            max_length=60,
            content="",
        )

        self.first_name: Element = Element(
            name="NM104",
            description="Name First",
            required=False,
            min_length=1,
            max_length=35,
            content="",
        )

        self.middle_name: Element = Element(
            name="NM105",
            description="Name Middle",
            required=False,
            min_length=1,
            max_length=25,
            content="",
        )

        self.name_prefix: Element = Element(
            name="NM106",
            description="Name Prefix",
            required=False,
            min_length=1,
            max_length=10,
            content="",
        )

        self.name_suffix: Element = Element(
            name="NM107",
            description="Name Suffix",
            required=False,
            min_length=1,
            max_length=10,
            content="",
        )

        self.id_code_qualifier: Element = Element(
            name="NM108",
            description="Identification Code Qualifier",
            required=True,
            min_length=1,
            max_length=2,
            content="",
        )

        self.id_code: Element = Element(
            name="NM109",
            description="Identification Code",
            required=True,
            min_length=2,
            max_length=80,
            content="",
        )

        self._relationship_code: Element = Element(
            name="NM110",
            description="Entity Relationship Code",
            required=False,
            min_length=2,
            max_length=2,
            content="",
        )

        self._entity_identifier_code: Element = Element(
            name="NM111",
            description="Entity Identifier Code",
            required=False,
            min_length=2,
            max_length=3,
            content="",
        )

        self._last_name_or_org_name: Element = Element(
            name="NM112",
            description="Name Last or Organization Name",
            required=False,
            min_length=1,
            max_length=60,
            content="",
        )

        self.nm101: Element = self.entity_identifier_code
        self.nm102: Element = self.entity_type_qualifier
        self.nm103: Element = self.last_name_or_org_name
        self.nm104: Element = self.first_name
        self.nm105: Element = self.middle_name
        self.nm106: Element = self.name_prefix
        self.nm107: Element = self.name_suffix
        self.nm108: Element = self.id_code_qualifier
        self.nm109: Element = self.id_code
        self.nm110: Element = self._relationship_code
        self.nm111: Element = self._entity_identifier_code
        self.nm112: Element = self._last_name_or_org_name

        self.fields.extend(
            (
                self.id,
                self.nm101,
                self.nm102,
                self.nm103,
                self.nm104,
                self.nm105,
                self.nm106,
                self.nm107,
                self.nm108,
                self.nm109,
                self.nm110,
                self.nm111,
                self.nm112,
            )
        )

    def to_dict(self) -> dict:
        return {
            "field_count": self.field_count,
            "id": self.id.to_dict(),
            "entity_identifier_code": self.entity_identifier_code.to_dict(),
            "entity_type_qualifier": self.entity_type_qualifier.to_dict(),
            "last_name_or_org_name": self.last_name_or_org_name.to_dict(),
            "first_name": self.first_name.to_dict(),
            "middle_name": self.middle_name.to_dict(),
            "name_prefix": self.name_prefix.to_dict(),
            "name_suffix": self.name_suffix.to_dict(),
            "id_code_qualifier": self.id_code_qualifier.to_dict(),
            "id_code": self.id_code.to_dict(),
        }


class GenericHierarchyLevel(Segment):
    """HL - Generic Hierarchy Level"""

    def __init__(self) -> None:
        Segment.__init__(self)
        self.field_count: int = 4

        self.id: Element = Element(
            name="HL",
            description="Hierarchical Level",
            required=True,
            min_length=2,
            max_length=2,
            content="HL",
        )

        self.id_number: Element = Element(
            name="HL01",
            description="Hierarchical ID Number",
            required=True,
            min_length=1,
            max_length=12,
            content="",
        )

        self.parent_id: Element = Element(
            name="HL02",
            description="Hierarchical Parent ID Number",
            required=False,
            min_length=1,
            max_length=12,
            content="",
        )

        self.level_code: Element = Element(
            name="HL03",
            description="Hierarchical Level Code",
            required=True,
            min_length=1,
            max_length=2,
            content="",
        )

        self.child_code: Element = Element(
            name="HL04",
            description="Hierarchical Child Code",
            required=True,
            min_length=1,
            max_length=1,
            content="",
        )

        self.hl01: Element = self.id_number
        self.hl02: Element = self.parent_id
        self.hl03: Element = self.level_code
        self.hl04: Element = self.child_code

        self.fields.extend((self.id, self.hl01, self.hl02, self.hl03, self.hl04))

    def to_dict(self) -> dict:
        return {
            "field_count": self.field_count,
            "id": self.id.to_dict(),
            "id_number": self.id_number.to_dict(),
            "parent_id": self.parent_id.to_dict(),
            "level_code": self.level_code.to_dict(),
            "child_code": self.child_code.to_dict(),
        }


class GenericRequestValidation(Segment):
    """AAA - Generic Request Validation"""

    def __init__(self) -> None:
        Segment.__init__(self)
        self.field_count: int = 4

        self.id: Element = Element(
            name="AAA",
            description="Request Validation",
            required=True,
            min_length=3,
            max_length=3,
            content="AAA",
        )

        self.id_number: Element = Element(
            name="AAA01",
            description="Yes/No Condition or Response Code",
            required=True,
            min_length=1,
            max_length=1,
            content="",
        )

        self.parent_id: Element = Element(
            name="AAA02",
            description="Agency Qualifier Code",
            required=False,
            min_length=2,
            max_length=2,
            content="",
        )

        self.level_code: Element = Element(
            name="AAA03",
            description="Reject Reason Code",
            required=True,
            min_length=2,
            max_length=2,
            content="",
        )

        self.child_code: Element = Element(
            name="AAA04",
            description="Follow-up Action Code",
            required=True,
            min_length=1,
            max_length=1,
            content="",
        )

        self.aaa01: Element = self.id_number
        self.aaa02: Element = self.parent_id
        self.aaa03: Element = self.level_code
        self.aaa04: Element = self.child_code

        self.fields.extend((self.id, self.aaa01, self.aaa02, self.aaa03, self.aaa04))

    def to_dict(self) -> dict:
        return {
            "field_count": self.field_count,
            "id": self.id.to_dict(),
            "id_number": self.id_number.to_dict(),
            "parent_id": self.parent_id.to_dict(),
            "level_code": self.level_code.to_dict(),
            "child_code": self.child_code.to_dict(),
        }
