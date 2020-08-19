# -*- coding: utf-8 -*-
from typing import List

from badx12.document.datastructures import Envelope
from badx12.document.transaction_set import TransactionSet as _TransactionSet

from .loops import InformationSourceLoop
from .segments import TransactionSetBHT


class TransactionSet(_TransactionSet):
    def __init__(self) -> None:
        _TransactionSet.__init__(self)
        self.sources: List[Envelope] = self.body
        self.hierarchical_transaction: TransactionSetBHT = TransactionSetBHT()

    def number_of_segments(self) -> int:
        header_trailer_count: int = 3
        sources_count: int = 0

        for source in self.sources:
            if isinstance(source, InformationSourceLoop):
                sources_count += source.number_of_segments() - 1

        return len(self.transaction_body) + header_trailer_count + sources_count

    def to_dict(self) -> dict:
        return {
            "header": self.header.to_dict(),
            "trailer": self.trailer.to_dict(),
            "hierarchical_transaction": self.hierarchical_transaction.to_dict(),
            "sources": [source.to_dict() for source in self.sources],
        }
