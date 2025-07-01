#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError

# Test invalid index cases
invalid_cases = [
    '$[1.0]',       # Float as index
    '$[1.5]',       # Float as index
    '$[-0]',        # Negative zero
    '$[9007199254740992]',  # Very large index (beyond safe integer range)
]

for test in invalid_cases:
    try:
        result = parse(test)
        print(f'ERROR: {test} should be invalid but was parsed as {result}')
    except JsonPathParserError as e:
        print(f'CORRECT: {test} -> {e}')
    except Exception as e:
        print(f'UNEXPECTED: {test} -> {e}')