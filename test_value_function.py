#!/usr/bin/env python3

from jsonpath_ng import parse

# Test the value() function  
document = {'c': 'cd', 'values': [{'a': 'ab'}, {'c': 'd'}, {'a': None}]}

# Test manual value function first
print("Testing value function manually:")
test_cases = [
    ('$[?value($.c)]', 'Should find single value'),
    ('$[?value($..c)]', 'Should find multiple values -> undefined'),
    ('$[?value($.missing)]', 'Should find no values -> undefined'),
]

for selector, description in test_cases:
    try:
        parsed = parse(selector)
        results = [match.value for match in parsed.find(document)]
        print(f'{selector}: {results} ({description})')
    except Exception as e:
        print(f'{selector}: Error - {e}')

print("\nTesting the actual failing test:")
# Now test the actual failing case
selector = '$.values[?length(@.a) == value($..c)]'
try:
    parsed = parse(selector)
    results = [match.value for match in parsed.find(document)]
    print(f'Results: {results}')
    print(f'Expected: [{{\"c\": \"d\"}}, {{\"a\": None}}]')
    
    # Debug: what does $..c return?
    c_selector = '$..c'
    c_parsed = parse(c_selector)
    c_results = [match.value for match in c_parsed.find(document)]
    print(f'$..c returns: {c_results}')
    
except Exception as e:
    print(f'Error: {e}')