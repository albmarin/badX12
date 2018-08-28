class DefaultSettings(object):
    """Default settings defined"""
    element_separator = "*"
    segment_terminator = "~"
    sub_element_separator = ">"
    version = "00501"


class DocumentSettings(object):
    """Current Settings"""
    element_separator = DefaultSettings.element_separator
    segment_terminator = DefaultSettings.segment_terminator
    sub_element_separator = DefaultSettings.sub_element_separator
    version = DefaultSettings.version
