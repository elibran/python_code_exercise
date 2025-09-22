from __future__ import annotations
import json
from typing import Any, Dict, TypeVar, Type

T = TypeVar("T")

class JSONSerializable:
    """Mixin providing JSON serialization using public API."""
    def to_json(self) -> str:
        # TODO: return a JSON string representing public attributes
        raise NotImplementedError

    @classmethod
    def from_json(cls: Type[T], data: str) -> T:
        # TODO: construct an instance from JSON string
        raise NotImplementedError

from datetime import datetime

class Auditable:
    """Mixin adding audit timestamps."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: set created_at and updated_at
        # ensure updates occur when balance changes (hint: call _touch())
    def _touch(self):
        # TODO: update updated_at
        pass
