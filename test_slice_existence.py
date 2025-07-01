#!/usr/bin/env python3

from jsonpath_ng import parse

# Test slice existence behavior  
selector = '$[?@[0:2]]'
document = [1, [], [2], [2, 3, 4], {}, {'a': 3}]

try:
    parsed = parse(selector)
    results = [match.value for match in parsed.find(document)]
    print(f'Results: {results}')
    print(f'Expected: [[2], [2, 3, 4]]')
    print(f'Test passes: {results == [[2], [2, 3, 4]]}')
    
    # Let's debug what @[0:2] returns for each element
    slice_selector = '@[0:2]'
    slice_parsed = parse(slice_selector)
    
    print(f'\nDebugging @[0:2] for each element:')
    for i, element in enumerate(document):
        slice_results = [match.value for match in slice_parsed.find(element)]
        print(f'Element {i} ({element}): @[0:2] -> {slice_results}')
        
except Exception as e:
    print(f'Error: {e}')