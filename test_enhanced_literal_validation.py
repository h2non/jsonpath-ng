#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError

# Test enhanced literal validation cases
invalid_cases = [
    '$[?true && false]',              # Bare literals in logical AND
    '$[?true || false]',              # Bare literals in logical OR
    '$[?true == false && false]',     # Mixed: comparison and bare literal
    '$[?true == false || false]',     # Mixed: comparison and bare literal
    '$[?false && true == false]',     # Mixed: bare literal and comparison
    '$[?false || true == false]',     # Mixed: bare literal and comparison
    '$[?!true]',                      # Bare literal in NOT
]

valid_cases = [
    '$[?@.a && @.b]',                 # Two path expressions
    '$[?@.a || @.b]',                 # Two path expressions
    '$[?true == false && @.a]',       # Comparison and path expression
    '$[?@.a == true || @.b == false]', # Two comparisons
    '$[?!@.a]',                       # NOT with path expression
]

print("Testing invalid cases (should fail):")
for test in invalid_cases:
    try:
        result = parse(test)
        print(f'ERROR: {test} should be invalid but was parsed as {result}')
    except JsonPathParserError as e:
        print(f'CORRECT: {test} -> {e}')
    except Exception as e:
        print(f'UNEXPECTED: {test} -> {e}')

print("\nTesting valid cases (should pass):")
for test in valid_cases:
    try:
        result = parse(test)
        print(f'CORRECT: {test} -> parsed successfully')
    except Exception as e:
        print(f'ERROR: {test} should be valid but failed: {e}')