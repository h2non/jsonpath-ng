#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.jsonpath import DatumInContext

# Debug the comparison logic
test_element = "quoted' literal"
selector_part = '@ == "quoted\' literal"'

try:
    # Test the filter expression by itself
    filter_parsed = parse(f'$[?{selector_part}]')
    
    # Test on a simple array with just this element
    simple_doc = [test_element]
    results = [match.value for match in filter_parsed.find(simple_doc)]
    print(f'Simple test with [{repr(test_element)}]:')
    print(f'Filter: $[?{selector_part}]')
    print(f'Results: {results}')
    print(f'Expected: [{repr(test_element)}]')
    print()
    
    # Let's manually test the comparison
    print('Manual comparison test:')
    left_str = test_element
    right_str = "quoted' literal"
    print(f'Left: {repr(left_str)}')
    print(f'Right: {repr(right_str)}')
    print(f'Equal: {left_str == right_str}')
    print(f'Left len: {len(left_str)}, Right len: {len(right_str)}')
    
except Exception as e:
    print(f'Error: {e}')