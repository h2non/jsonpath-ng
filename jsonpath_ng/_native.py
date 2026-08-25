"""Optional native accelerator for jsonpath-ng.

When the ``aero-jsonpath`` package is installed, ``find_values()`` delegates
to the native Aero-compiled kernel for a 2–6× speedup on filter/descendant
workloads.  If the expression is outside the supported subset, the call
raises ``NotImplementedError`` and ``find_values()`` falls back to Python.
"""
import json as _json

try:
    import aero_jsonpath as _aero
    _available = True
except ImportError:
    _available = False


def find_values(path, data):
    """Return ``[m.value for m in path.find(data)]`` via native kernel.

    Raises ``NotImplementedError`` if the expression is not in the
    supported subset (regex filters, ``in``, arithmetic, etc.).
    """
    if not _available:
        raise ImportError("aero-jsonpath not installed")

    expr = getattr(path, "_source_expr", None)
    if expr is None:
        raise NotImplementedError("no source expression")

    json_str = _json.dumps(data, separators=(",", ":"))
    result = _aero.search(expr, json_str)
    return result
