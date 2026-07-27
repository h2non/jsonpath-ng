from typing import assert_type

from jsonpath_ng import Child, DatumInContext, Fields, Index, JSONPath, Root, Slice, parse
from jsonpath_ng.ext import parse as ext_parse
from jsonpath_ng.ext.filter import Expression, Filter

document: dict[str, list[dict[str, object]]] = {
    "items": [{"name": "alpha", "score": 1}, {"name": "beta", "score": 2}]
}

path = Child(Root(), Child(Fields("items"), Slice()))
assert_type(path, Child)
assert_type(parse("$.items[*].name"), JSONPath)
assert_type(ext_parse("$.items[?score >= 2].name"), JSONPath)

matches = path.find(document)
assert_type(matches, list[DatumInContext[object]])
datum = DatumInContext("before")
datum.value = "after"
assert_type(
    Root().find(document),
    list[DatumInContext[object]],
)
assert_type(Index(0).update(document["items"], {"name": "updated"}), list[dict[str, object]])
assert_type(
    Fields("name").filter(lambda value: value == "beta", document["items"][1]),
    dict[str, object],
)

expression = Expression(Fields("score"), ">=", 2)
filter_path = Filter([expression])
assert_type(filter_path.find(document["items"]), list[DatumInContext[object]])

def update_value(value: object, container: object, key: str) -> str:
    return f"{key}:{value}"

assert_type(
    Fields("name").update(document["items"][0], update_value),
    dict[str, object],
)
