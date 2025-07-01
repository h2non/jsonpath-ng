#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.jsonpath import DatumInContext, CurrentNode, Literal, Comparison

# Debug filter evaluation step by step
test_element = "quoted' literal"
document = [test_element]

# Parse the filter expression
filter_selector = '$[?@ == "quoted\' literal"]'
parsed = parse(filter_selector)

print(f'Parsed filter: {parsed}')
print(f'Filter expression: {parsed.right.expression}')
print(f'Expression type: {type(parsed.right.expression)}')

if hasattr(parsed.right.expression, 'left'):
    print(f'Left side: {parsed.right.expression.left} (type: {type(parsed.right.expression.left)})')
if hasattr(parsed.right.expression, 'right'):
    print(f'Right side: {parsed.right.expression.right} (type: {type(parsed.right.expression.right)})')
if hasattr(parsed.right.expression, 'operator'):
    print(f'Operator: {parsed.right.expression.operator}')

# Test evaluation manually
element_datum = DatumInContext(test_element)
if hasattr(parsed.right.expression, 'evaluate'):
    result = parsed.right.expression.evaluate(element_datum)
    print(f'Manual evaluation result: {result}')
    
    # Debug the comparison values
    if isinstance(parsed.right.expression, Comparison):
        left_val = parsed.right.expression._get_value(parsed.right.expression.left, element_datum)
        right_val = parsed.right.expression._get_value(parsed.right.expression.right, element_datum)
        print(f'Left value: {repr(left_val)} (type: {type(left_val)})')
        print(f'Right value: {repr(right_val)} (type: {type(right_val)})')
        print(f'Direct comparison: {left_val == right_val}')
        print(f'Left is UNDEFINED: {left_val is parsed.right.expression.__class__.__module__.find("UNDEFINED")}')
        print(f'Right is UNDEFINED: {right_val is parsed.right.expression.__class__.__module__.find("UNDEFINED")}')
else:
    print('Expression does not have evaluate method')