# -*- coding: utf-8 -*-
from typing import List, Optional, Tuple

from badx12.document.datastructures.envelope import GenericLoopEnvelope
from badx12.document.revisions.M271_00510X279A1.loops import (
    DependentLoop,
    InformationReceiverLoop,
    InformationSourceLoop,
    SubscriberLoop,
)
from badx12.document.revisions.M271_00510X279A1.segments import (
    InformationSourceHL,
    InformationSourceName,
    InformationSourceRequestValidation,
    TransactionSetBHT,
)
from badx12.document.revisions.M271_00510X279A1.transaction_set import TransactionSet
from badx12.document.transaction_set import TransactionSetHeader

from .base import Parser as _Parser


class Parser(_Parser):
    def __init__(self, document: Optional[str] = None):
        _Parser.__init__(self, document)
        self.current_hierarchy: Tuple[int, int] = (0, 0)
        self.current_loop: GenericLoopEnvelope = GenericLoopEnvelope()
        self.current_transaction: TransactionSet = TransactionSet()

    def _get_segment_functions(self) -> dict:
        return {
            TransactionSetBHT().id.name: self._parse_beginning_of_hierarchical_transaction,
            InformationSourceHL().id.name: self._parse_hierarchical_level,
            InformationSourceName().id.name: self._parse_source_name,
            InformationSourceRequestValidation().id.name: self._parse_request_validation,
        }

    def _parse_transaction_set_header(self, segment: str) -> None:
        """Parse transaction set header
        Creates a new transaction set and set it as the current transaction set.
        """
        self.current_transaction = TransactionSet()
        transaction_header: TransactionSetHeader = TransactionSetHeader()
        header_field_list: List[str] = segment.split(
            self.document.config.element_separator
        )
        self._parse_segment(transaction_header, header_field_list)
        self.current_transaction.header = transaction_header

    def _parse_beginning_of_hierarchical_transaction(self, segment: str) -> None:
        transaction_bht: TransactionSetBHT = TransactionSetBHT()
        bht_field_list: List[str] = segment.split(
            self.document.config.element_separator
        )
        self._parse_segment(transaction_bht, bht_field_list)
        self.current_transaction.hierarchical_transaction = transaction_bht

    def _parse_hierarchical_level(self, segment: str) -> None:
        loops = [
            (InformationSourceLoop, ""),
            (InformationReceiverLoop, "receivers"),
            (SubscriberLoop, "subscribers"),
        ]
        hl_field_list: List[str] = segment.split(self.document.config.element_separator)
        hierarchy = (int(hl_field_list[1]), int(hl_field_list[2].strip() or 0))

        hierarchical_level = InformationSourceHL()
        self._parse_segment(hierarchical_level, hl_field_list)

        if hierarchy[1] == 0:
            self.hierarchy_sequence = 0
            self.current_loop = loops[self.hierarchy_sequence][0]()
            self.current_transaction.sources.append(self.current_loop)

        elif self.current_hierarchy[0] == hierarchy[1]:
            self.hierarchy_sequence += 1
            loop_class = loops[self.hierarchy_sequence][0]()
            self.current_loop.body.append(loop_class)
            self.current_loop = loop_class

        self.current_hierarchy = hierarchy
        self.current_loop.hierarchical_level = hierarchical_level

    def _parse_request_validation(self, segment: str) -> None:
        request_validation = InformationSourceRequestValidation()
        aaa_field_list: List[str] = segment.split(
            self.document.config.element_separator
        )
        self._parse_segment(request_validation, aaa_field_list)
        self.current_loop.request_validations.append(request_validation)

    def _parse_source_name(self, segment: str) -> None:
        source_name = InformationSourceName()
        nm1_field_list: List[str] = segment.split(
            self.document.config.element_separator
        )
        self._parse_segment(source_name, nm1_field_list)
        self.current_loop.name = source_name
