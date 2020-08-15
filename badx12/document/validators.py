# -*- coding: utf-8 -*-
class ValidationReport:
    def __init__(self) -> None:
        self.error_list: list = []

    def add_error(self, error: Exception) -> None:
        self.error_list.append(error)

    def is_document_valid(self) -> bool:
        return len(self.error_list) == 0
