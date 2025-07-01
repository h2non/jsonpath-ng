#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError

# Test literal validation cases
invalid_cases = [
    '$[?true]',    # Bare boolean literal
    '$[?false]',   # Bare boolean literal
    "$[?'abc']",   # Bare string literal
    '$[?2]',       # Bare integer literal
    '$[?2.2]',     # Bare float literal
]

valid_cases = [
    '$[?true==true]',     # Boolean literal in comparison
    '$[?@.a==false]',     # Boolean literal compared to field
    "$[?@=='abc']",       # String literal compared to current node
    '$[?@.count==2]',     # Integer literal in comparison
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