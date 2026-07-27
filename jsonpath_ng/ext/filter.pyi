from __future__ import annotations

import operator as operator
import re as re
from collections.abc import Callable
from typing import Literal, TypeAlias, TypeVar

from ..jsonpath import (
    DatumInContext as DatumInContext,
    Index as Index,
    JSONPath as JSONPath,
)

_DataT = TypeVar("_DataT")
_ValueT = TypeVar("_ValueT")
_FilterOperator: TypeAlias = Literal["!=", "==", "=", "<=", "<", ">=", ">", "=~"]
OPERATOR_MAP: dict[str, Callable[[object, object], bool]]

class Filter(JSONPath):
    expressions: list[Expression]
    def __init__(self, expressions: list[Expression]) -> None: ...
    def find(self, datum: object) -> list[DatumInContext[object]]: ...  # pyright: ignore[reportIncompatibleMethodOverride]
    def filter(self, fn: Callable[[object], bool], data: _DataT) -> _DataT: ...
    def update(
        self,
        data: _DataT,
        val: _ValueT | Callable[[object, object, int], _ValueT | None],
    ) -> _DataT: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...

class Expression(JSONPath):
    target: JSONPath
    op: _FilterOperator | None
    value: object
    def __init__(
        self, target: JSONPath, op: _FilterOperator | None, value: object
    ) -> None: ...
    def find(self, datum: object) -> list[DatumInContext[object]]: ...  # pyright: ignore[reportIncompatibleMethodOverride]
    def __eq__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
