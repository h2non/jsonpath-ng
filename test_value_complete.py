#!/usr/bin/env python3

from jsonpath_ng import parse

# Test the complete value function expression
document = {'c': 'cd', 'values': [{'a': 'ab'}, {'c': 'd'}, {'a': None}]}

# Test the actual failing case
selector = '$.values[?length(@.a) == value($..c)]'
try:
    parsed = parse(selector)
    results = [match.value for match in parsed.find(document)]
    print(f'Selector: {selector}')
    print(f'Results: {results}')
    print(f'Expected: [{{\"c\": \"d\"}}, {{\"a\": None}}]')
    print(f'Test passes: {results == [{"c": "d"}, {"a": None}]}')
    
except Exception as e:
    print(f'Error: {e}')

# Debug step by step
print(f'\nDebugging:')
print(f'$..c returns: {[match.value for match in parse("$..c").find(document)]}')
print(f'Since $..c returns multiple values, value($..c) = UNDEFINED')

print(f'\nFor each element in values array:')
for i, element in enumerate(document['values']):
    print(f'Element {i}: {element}')
    
    # Test length(@.a) for this element
    try:
        length_filter = f'$[?length(@.a)]'
        length_parsed = parse(length_filter)  
        length_matches = length_parsed.find([element])
        
        if length_matches:
            print(f'  length(@.a) is truthy (element matches length filter)')
        else:
            print(f'  length(@.a) is falsy/undefined (element does not match length filter)')
            
    except Exception as e:
        print(f'  length(@.a): Error - {e}')