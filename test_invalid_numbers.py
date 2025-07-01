#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError

# Test invalid number formats that should be rejected
invalid_cases = [
    '$[?@.a==.1]',     # Leading decimal point
    '$[?@.a==-.1]',    # Negative leading decimal point
    '$[?@.a==00]',     # Leading zero
    '$[?@.a==01]',     # Leading zero with digit
    '$[?@.a==1.]',     # Trailing decimal point
    '$[?@.a==1.e1]',   # Decimal point followed by exponent
]

for test in invalid_cases:
    try:
        result = parse(test)
        print(f'ERROR: {test} should be invalid but was parsed as {result}')
    except JsonPathParserError as e:
        print(f'CORRECT: {test} -> {e}')
    except Exception as e:
        print(f'UNEXPECTED: {test} -> {e}')