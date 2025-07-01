#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError

# Test descendant notation validation in different contexts
test_cases = [
    ('$[?@..a==1]', False),         # Should be invalid - descendant in comparison
    ('$[?@.a==$..b]', False),       # Should be invalid - descendant in comparison  
    ('$[?length($..a)]', True),     # Should be valid - descendant in function
    ('$[?count($..a)==1]', True),   # Should be valid - descendant in function argument
]

for test, should_pass in test_cases:
    try:
        result = parse(test)
        if should_pass:
            print(f'CORRECT: {test} -> parsed successfully')
        else:
            print(f'ERROR: {test} should be invalid but was parsed')
    except JsonPathParserError as e:
        if not should_pass:
            print(f'CORRECT: {test} -> {e}')
        else:
            print(f'ERROR: {test} should be valid but failed: {e}')
    except Exception as e:
        print(f'UNEXPECTED: {test} -> {e}')