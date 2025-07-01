#!/usr/bin/env python3

from jsonpath_ng import parse

# Test the specific failing string literal case
document = ["quoted' literal", 'a', "quoted\\' literal"]
selector = '$[?@ == "quoted\' literal"]'

try:
    parsed = parse(selector)
    results = [match.value for match in parsed.find(document)]
    print(f'Selector: {selector}')
    print(f'Document: {document}')
    print(f'Results: {results}')
    expected = ["quoted' literal"]
    print(f'Expected: {expected}')
    print(f'Test passes: {results == expected}')
    
    # Debug what @ returns for each element
    print(f'\nDebugging @ for each element:')
    for i, element in enumerate(document):
        print(f'Element {i}: {repr(element)}')
        at_parsed = parse('@')
        at_results = [match.value for match in at_parsed.find(element)]
        print(f'  @ -> {at_results}')
        
except Exception as e:
    print(f'Error: {e}')