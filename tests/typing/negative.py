from jsonpath_ng import Fields, Index, parse
from jsonpath_ng.ext.filter import Expression

Fields(1)  # E: field names must be strings
Index("0")  # E: indices must be integers
parse(1)  # E: expressions must be strings
Expression(Fields("score"), "contains", 2)  # E: unsupported filter operator
Fields("name").filter(lambda value: "yes", {"name": "alpha"})  # E: predicates return bool
