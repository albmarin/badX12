# -*- coding: utf-8 -*-
from typing import List

from badx12.document.datastructures import (
    DependentLoopEnvelope,
    InformationReceiverLoopEnvelope,
    InformationSourceLoopEnvelope,
    SubscriberLoopEnvelope,
)

from .segments import (
    InformationSourceHL,
    InformationSourceName,
    InformationSourceRequestValidation,
)


class InformationSourceLoop(InformationSourceLoopEnvelope):
    def __init__(self) -> None:
        InformationSourceLoopEnvelope.__init__(self)
        self.name: InformationSourceName = InformationSourceName()
        self.hierarchical_level: InformationSourceHL = InformationSourceHL()
        self.request_validations: List[InformationSourceRequestValidation] = []
        self.receivers: List[InformationReceiverLoopEnvelope] = self.loop_body

    def to_dict(self) -> dict:
        return {
            "hierarchical_level": self.hierarchical_level.to_dict(),
            "name": self.name.to_dict(),
            "request_validations": [
                req_validation.to_dict() for req_validation in self.request_validations
            ],
            "receivers": [receiver.to_dict() for receiver in self.receivers],
        }


class InformationReceiverLoop(InformationReceiverLoopEnvelope):
    def __init__(self) -> None:
        InformationReceiverLoopEnvelope.__init__(self)
        self.name: InformationSourceName = InformationSourceName()
        self.hierarchical_level: InformationSourceHL = InformationSourceHL()
        self.subscribers: List[SubscriberLoop] = self.loop_body

    def number_of_segments(self) -> int:
        header_trailer_count: int = 2
        subscriber_count: int = 0

        for subscriber in self.subscribers:
            if isinstance(subscriber, SubscriberLoop):
                subscriber_count += subscriber.number_of_segments()

        return header_trailer_count + subscriber_count

    def to_dict(self) -> dict:
        return {
            "hierarchical_level": self.hierarchical_level.to_dict(),
            "name": self.name.to_dict(),
            "subscribers": [sub.to_dict() for sub in self.subscribers],
        }


class SubscriberLoop(SubscriberLoopEnvelope):
    def __init__(self) -> None:
        SubscriberLoopEnvelope.__init__(self)
        self.name: InformationSourceName = InformationSourceName()
        self.hierarchical_level: InformationSourceHL = InformationSourceHL()
        self.dependents: List[DependentLoop] = self.loop_body

    def number_of_segments(self) -> int:
        header_trailer_count: int = 3
        dependent_count: int = 0

        for dependent in self.dependents:
            if isinstance(dependent, SubscriberLoop):
                dependent_count += dependent.number_of_segments()

        return header_trailer_count + dependent_count

    def to_dict(self) -> dict:
        return {
            "hierarchical_level": self.hierarchical_level.to_dict(),
            "name": self.name.to_dict(),
            "dependents": [dep.to_dict() for dep in self.dependents],
        }


class DependentLoop(DependentLoopEnvelope):
    def __init__(self) -> None:
        DependentLoopEnvelope.__init__(self)
        self.hierarchical_level: InformationSourceHL = InformationSourceHL()

    def number_of_segments(self) -> int:
        header_trailer_count: int = 2
        dependent_count: int = 0

        return header_trailer_count + dependent_count

    def to_dict(self) -> dict:
        return {}
