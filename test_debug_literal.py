#!/usr/bin/env python3

from jsonpath_ng import parse

# Test parsing just 'a.*' by itself to see what it becomes
test_cases = [
    "'a.*'",
    "a.*",
    "@.a",
]

for test in test_cases:
    try:
        result = parse(test)
        print(f"'{test}' -> {result} (type: {type(result)})")
    except Exception as e:
        print(f"'{test}' failed: {e}")

# Test the function again with debug
print("\nFunction test:")
try:
    result = parse("$[?match(@.a, 'a.*')]")
    print(f"Parsed: {result}")
    expr = result.right.expression
    print(f"Expression: {expr}")
    for i, arg in enumerate(expr.arguments):
        print(f"Arg {i}: {type(arg).__name__} = {arg}")
        if hasattr(arg, 'fields'):
            print(f"  Fields: {arg.fields}")
except Exception as e:
    print(f"Failed: {e}")