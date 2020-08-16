# -*- coding: utf-8 -*-

from typing import Union

from badx12.document.validators import ValidationReport
from badx12.exceptions import FieldValidationError


class Element(object):
    """A generic segment"""

    def __init__(
        self,
        name: str = "",
        description: str = "",
        required: bool = False,
        min_length: int = 0,
        max_length: int = 0,
        content: Union[str, int] = "",
    ):
        self.name: str = name
        self.description: str = description
        self.required: bool = required
        self.min_length: int = min_length
        self.max_length: int = max_length
        self.content: Union[str, int] = content

    def validate(self, report: ValidationReport) -> None:
        """Validate the element"""
        if self.required or self.content != "":
            content_length: int = len(str(self.content))
            self._is_field_too_short(content_length, report)
            self._is_field_too_long(content_length, report)

    def _is_field_too_short(
        self, content_length: int, report: ValidationReport
    ) -> None:
        """
        Determine if the field content is too short.
        :param content_length: current content length.
        :param report: the validation report to append errors.
        """
        if content_length < self.min_length:
            report.add_error(
                FieldValidationError(
                    msg=f"""Field {self.name} is too short. Found {content_length} characters, expected
                    {self.min_length} characters.""",
                    segment=self,
                )
            )

    def _is_field_too_long(self, content_length: int, report: ValidationReport) -> None:
        """
        Determine if the field content is too long.
        :param content_length: current content length.
        :param report: the validation report to append errors.
        """
        if content_length > self.max_length:
            report.add_error(
                FieldValidationError(
                    msg=f"""Field {self.name} is too long. Found {content_length} characters,
                    expected {self.max_length} characters.""",
                    segment=self,
                )
            )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "required": self.required,
            "min_length": self.min_length,
            "max_length": self.max_length,
            "content": self.content,
        }

    def __str__(self) -> str:
        return str(self.content)

    def __repr__(self) -> str:
        return (
            f"Element(name={self.name}, description={self.description}, required={self.required}, "
            f"min_length={self.min_length}, max_length={self.max_length}, content={self.content})"
        )
