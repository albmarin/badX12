# -*- coding: utf-8 -*-
class DocumentSettings(object):
    """Current Settings"""

    element_separator: str = "*"
    segment_terminator: str = "~"
    sub_element_separator: str = ">"
    version: str = "00501"


class DocumentConfiguration:
    def __init__(
        self,
        version: str,
        element_separator: str,
        segment_terminator: str,
        sub_element_separator: str,
    ):
        """Creates a new Edi Document Configuration"""
        self.version: str = version
        self.element_separator: str = element_separator
        self.segment_terminator: str = segment_terminator
        self.sub_element_separator: str = sub_element_separator

    def to_dict(self) -> dict:
        return {
            "element_separator": self.element_separator,
            "segment_terminator": self.segment_terminator,
            "sub_element_separator": self.sub_element_separator,
            "version": self.version,
        }
