import pprint as pp

from .errors import FieldValidationError


class Element(object):
    """A generic segment"""

    def __init__(
        self,
        name="",
        description="",
        required="",
        min_length="",
        max_length="",
        content="",
    ):
        self.name = name
        self.description = description
        self.required = required
        self.min_length = min_length
        self.max_length = max_length
        self.content = content

    def validate(self, report):
        """Validate the element"""
        if self.required or self.content != "":
            content_length = len(self.content)
            self._is_field_too_short(content_length, report)
            self._is_field_too_long(content_length, report)

    def __str__(self):
        if self.required:
            return str(self.content)

        if self.content != "":
            return str(self.content)

        return ""

    def _is_field_too_short(self, content_length, report):
        """
        Determine if the field content is too short.
        :param content_length: current content length.
        :param report: the validation report to append errors.
        """
        if content_length < self.min_length:
            report.add_error(
                FieldValidationError(
                    msg=f"Field {self.name} is too short. Found {content_length} characters, expected "
                    f"{self.min_length} characters.",
                    segment=self,
                )
            )

    def _is_field_too_long(self, content_length, report):
        """
        Determine if the field content is too long.
        :param content_length: current content length.
        :param report: the validation report to append errors.
        """
        if content_length > self.max_length:
            report.add_error(
                FieldValidationError(
                    msg=f"Field {self.name} is too long. Found {content_length} characters, "
                    f"expected {self.max_length} characters.",
                    segment=self,
                )
            )

    def to_dict(self):
        return {
            "element": {
                "name": self.name,
                "description": self.description,
                "required": self.required,
                "min_length": self.min_length,
                "max_length": self.max_length,
                "content": self.content,
            }
        }

    def __repr__(self):
        _pp = pp.PrettyPrinter()
        return _pp.pformat(self.to_dict())
