#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.jsonpath import FunctionCall, Fields, Literal, CurrentNode, Child

# Test function parsing step by step
selector = '$[?match(@.a, "a.*")]'
try:
    parsed = parse(selector)
    print(f'Parsed: {parsed}')
    
    # Check the filter structure
    if hasattr(parsed, 'right') and hasattr(parsed.right, 'expression'):
        filter_expr = parsed.right.expression
        print(f'Filter expression type: {type(filter_expr)}')
        print(f'Filter expression: {filter_expr}')
        
        if isinstance(filter_expr, FunctionCall):
            print(f'Function name: {filter_expr.function_name}')
            print(f'Arguments: {filter_expr.arguments}')
            for i, arg in enumerate(filter_expr.arguments):
                print(f'Arg {i}: {type(arg)} = {arg}')
                
    # Test evaluation
    document = [{'a': 'ab'}, {'a': 'cd'}]
    print(f'Testing on document: {document}')
    
    results = parsed.find(document)
    print(f'Results: {[r.value for r in results]}')
    
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()