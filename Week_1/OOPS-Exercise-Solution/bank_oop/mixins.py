from __future__ import annotations
import json
from typing import Any, Dict, TypeVar, Type
from datetime import datetime

T = TypeVar("T")

class JSONSerializable:
    """Mixin providing JSON serialization using public API."""
    def to_json(self) -> str:
        data = {}
        # naive approach: collect public attrs (no leading underscore)
        for k, v in self.__dict__.items():
            if not k.startswith("_"):
                data[k] = v if isinstance(v, (int, float, str, bool, type(None))) else str(v)
        return json.dumps(data, default=str)

    @classmethod
    def from_json(cls: Type[T], data: str) -> T:
        obj = json.loads(data)
        return cls(**obj)  # type: ignore[arg-type]

class Auditable:
    """Mixin adding audit timestamps."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = self.created_at

    def _touch(self):
        from datetime import datetime as _dt
        self.updated_at = _dt.utcnow()
