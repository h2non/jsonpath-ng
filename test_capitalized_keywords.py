#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError

# Test incorrectly capitalized keywords
test_cases = [
    ('$[?@==True]', 'Should fail - True instead of true'),
    ('$[?@==False]', 'Should fail - False instead of false'),
    ('$[?@==Null]', 'Should fail - Null instead of null'),
    ('$[?@==NULL]', 'Should fail - NULL instead of null'),
    ('$[?@==TRUE]', 'Should fail - TRUE instead of true'),
    ('$[?@==FALSE]', 'Should fail - FALSE instead of false'),
]

for selector, description in test_cases:
    try:
        result = parse(selector)
        print(f'Parsed: {selector} -> {result} ({description})')
        
        # Test what the comparison actually does
        test_doc = [True, False, None, 'True', 'False', 'Null']
        results = [match.value for match in result.find(test_doc)]
        print(f'  Results on {test_doc}: {results}')
        
    except Exception as e:
        print(f'Failed: {selector} -> {e} ({description})')
    print()