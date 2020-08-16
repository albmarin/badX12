# -*- coding: utf-8 -*-


class FieldValidationError(Exception):
    """Exception raised for errors in the input.
    Attributes:
        segment -- element in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, segment: object, msg: str):
        self.segment: object = segment
        self.msg: str = msg


class IDMismatchError(Exception):
    """Exception raised for errors in the input.
        Attributes:
            segment -- element in which the error occurred
            msg  -- explanation of the error
        """

    def __init__(self, segment: object, msg: str):
        self.segment: object = segment
        self.msg: str = msg


class SegmentCountError(Exception):
    """Exception raised for errors in the input.
        Attributes:
            segment -- element in which the error occurred
            msg  -- explanation of the error
        """

    def __init__(self, segment: object, msg: str):
        self.segment: object = segment
        self.msg: str = msg


class InvalidFileTypeError(Exception):
    """Exception raised for errors in the input.
    Attributes:
        segment -- segment in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, segment: str, msg: str):
        self.expr: str = segment
        self.msg: str = msg


class SegmentTerminatorNotFoundError(Exception):
    """Exception raised for errors in the Interchange Header.
    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg: str):
        self.msg: str = msg
