from typing import TypedDict, assert_type

from jsonpath_ng import Child, DatumInContext, Fields, Index, JSONPath, Root, Slice, parse
from jsonpath_ng.ext import parse as ext_parse
from jsonpath_ng.ext.filter import Expression, Filter

class Item(TypedDict):
    name: str
    score: int

class Document(TypedDict):
    items: list[Item]

document: Document = {
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
updated_item: Item = {"name": "updated", "score": 3}
assert_type(Index(0).update(document["items"], updated_item), list[Item])
record: dict[str, object] = {"name": "beta", "score": 2}
assert_type(
    Fields("name").filter(lambda value: value == "beta", record),
    dict[str, object],
)

expression = Expression(Fields("score"), ">=", 2)
filter_path = Filter([expression])
assert_type(filter_path.find(document["items"]), list[DatumInContext[object]])

def update_value(value: object, container: object, key: str) -> str:
    return f"{key}:{value}"

assert_type(
    Fields("name").update(document["items"][0], update_value),
    Item,
)
