#!/usr/bin/env python3

from jsonpath_ng import parse

# Test null comparison semantics
selector = '$[?@.a==null]'
document = [{'d': 'e'}, {'a': 'c', 'd': 'f'}]

try:
    parsed = parse(selector)
    results = [match.value for match in parsed.find(document)]
    print(f'Results: {results}')
    print(f'Expected: []')
    print(f'Test passes: {results == []}')
    
    # Let's also test what @.a returns for the first element
    at_a_selector = '@.a'
    at_a_parsed = parse(at_a_selector)
    first_element = document[0]
    at_a_results = [match.value for match in at_a_parsed.find(first_element)]
    print(f'@.a on {{\"d\": \"e\"}}: {at_a_results}')
    
except Exception as e:
    print(f'Error: {e}')