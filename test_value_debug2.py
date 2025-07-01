#!/usr/bin/env python3

from jsonpath_ng import parse

# Debug the value function test more carefully  
document = {'c': 'cd', 'values': [{'a': 'ab'}, {'c': 'd'}, {'a': None}]}

print("Document:", document)
print()

# Check what $..c returns
c_selector = '$..c'
c_parsed = parse(c_selector)
c_results = [match.value for match in c_parsed.find(document)]
print(f'$..c returns: {c_results} (length: {len(c_results)})')
print(f'value($..c) should return: UNDEFINED (because multiple values)')
print()

# Test individual length() expressions for each element
print("Testing length(@.a) for each element in values array:")
test_cases = [
    ('$.values[0][?length(@.a)]', '{"a": "ab"}', 'length("ab") = 2'),
    ('$.values[1][?length(@.a)]', '{"c": "d"}', 'length(undefined) = undefined'),  
    ('$.values[2][?length(@.a)]', '{"a": None}', 'length(None) = undefined'),
]

for selector, element, expected in test_cases:
    try:
        parsed = parse(selector)
        results = [match.value for match in parsed.find(document)]
        print(f'{selector}: {results} - {expected}')
    except Exception as e:
        print(f'{selector}: Error - {e}')

print()

# Now test with the actual comparison - but first need to understand what the expected logic is
print("Let me check what the actual test expects:")
print("Expected: [{'c': 'd'}, {'a': None}]")
print("These are elements where @.a is undefined or null")
print("So the test is checking: length(@.a) == undefined_value") 
print("Since $..c returns multiple values, value($..c) = undefined")
print("So we need: length(@.a) == undefined")

# Test just the length function with undefined/null
print()
print("Testing length function behavior:")
length_tests = [
    ('$[?length(@.missing)]', 'Should match if length(undefined) is truthy'),
    ('$[?length(@.a)]', 'Should match elements where length(@.a) is truthy'),
]

for selector, description in length_tests:
    try:
        parsed = parse(selector)
        results = [match.value for match in parsed.find(document['values'])]
        print(f'{selector}: {results} - {description}')
    except Exception as e:
        print(f'{selector}: Error - {e}')