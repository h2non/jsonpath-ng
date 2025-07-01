#!/usr/bin/env python3

from jsonpath_ng import parse

# Test logical operator precedence
document = [{'a': 1}, {'b': 2, 'c': 3}, {'c': 3}, {'b': 2}, {'a': 1, 'b': 2, 'c': 3}]
selector = '$[?@.a || @.b && @.c]'

try:
    parsed = parse(selector)
    results = [match.value for match in parsed.find(document)]
    print(f'Selector: {selector}')
    print(f'Results: {results}')
    print(f'Expected: [{{\"a\": 1}}, {{\"b\": 2, \"c\": 3}}, {{\"a\": 1, \"b\": 2, \"c\": 3}}]')
    
    # Let's also test what the parsed expression looks like
    print(f'Parsed expression: {parsed.right.expression}')
    
    # Test individual elements manually to understand the logic
    print(f'\nDebugging each element:')
    for i, element in enumerate(document):
        print(f'Element {i}: {element}')
        # Test individual conditions
        for condition in ['@.a', '@.b', '@.c']:
            try:
                cond_selector = f'$[?{condition}]'
                cond_parsed = parse(cond_selector)
                cond_results = cond_parsed.find([element])
                print(f'  {condition}: {bool(cond_results)}')
            except Exception as e:
                print(f'  {condition}: Error - {e}')
        
        # Test expected result for this element
        # @.a || (@.b && @.c) 
        has_a = 'a' in element
        has_b = 'b' in element
        has_c = 'c' in element
        expected_match = has_a or (has_b and has_c)
        print(f'  Expected match (@.a || (@.b && @.c)): {expected_match}')
        
        # Test what our parser produces
        actual_results = parsed.find([element])
        actual_match = bool(actual_results)
        print(f'  Actual match: {actual_match}')
        print()
        
except Exception as e:
    print(f'Error: {e}')