#!/usr/bin/env python3

from jsonpath_ng import parse

# Test all string literal cases from compliance tests
test_cases = [
    # (selector, document, expected)
    ('$[?@ == "quoted\' literal"]', ["quoted' literal", 'a'], ["quoted' literal"]),
    ('$[?@ == \'quoted" literal\']', ['quoted" literal', 'a'], ['quoted" literal']),
    ('$[?@ == "quoted\\" literal"]', ['quoted" literal', 'a'], ['quoted" literal']),
    ('$[?@ == \'quoted\\\' literal\']', ["quoted' literal", 'a'], ["quoted' literal"]),
]

for selector, document, expected in test_cases:
    try:
        parsed = parse(selector)
        results = [match.value for match in parsed.find(document)]
        print(f'Selector: {selector}')
        print(f'Results: {results}')
        print(f'Expected: {expected}')
        print(f'Test passes: {results == expected}')
        print()
    except Exception as e:
        print(f'Error with {selector}: {e}')
        print()