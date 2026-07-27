from __future__ import annotations

import operator as operator
from collections.abc import Callable

from ..jsonpath import DatumInContext as DatumInContext, JSONPath as JSONPath

OPERATOR_MAP: dict[str, Callable[[object, object], object]]

class Operation(JSONPath):
    left: JSONPath | object
    op_symbol: str
    op: Callable[[object, object], object]
    right: JSONPath | object
    def __init__(self, left: JSONPath | object, op: str, right: JSONPath | object) -> None: ...
    def find(self, datum: object) -> list[DatumInContext[object]]: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
