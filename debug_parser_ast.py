#!/usr/bin/env python3

from jsonpath_ng import parse

# Parse both selectors and examine their AST
jp1 = parse("@[0]")
jp2 = parse("@['0']")

print(f"@[0] AST: {repr(jp1)}")
print(f"@['0'] AST: {repr(jp2)}")

# Let's also check the specific filter expressions
jp3 = parse("$[?@[0] == 5]")
jp4 = parse("$[?@['0'] == 5]")

print(f"\n$[?@[0] == 5] AST: {repr(jp3)}")
print(f"$[?@['0'] == 5] AST: {repr(jp4)}")

# Let's look at the filter expression parts
print(f"\nFilter expr for @[0]: {repr(jp3.expression.left)}")
print(f"Filter expr for @['0']: {repr(jp4.expression.left)}")