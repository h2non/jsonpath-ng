#!/usr/bin/env python3

from jsonpath_ng.parser import JsonPathParser
from jsonpath_ng.lexer import JsonPathLexer

# Debug what AST @.* produces
parser = JsonPathParser()

test_input = '$[?length(@.*)<3]'
print(f"Input: {test_input}")

try:
    jp = parser.parse(test_input)
    print(f"Parsed: {jp}")
    print(f"Type: {type(jp)}")
    
    # Navigate the AST to find the function call
    if hasattr(jp, 'right') and hasattr(jp.right, 'expression'):
        filter_expr = jp.right.expression
        print(f"Filter: {filter_expr}")
        print(f"Filter type: {type(filter_expr)}")
        
        if hasattr(filter_expr, 'left'):
            func_call = filter_expr.left
            print(f"Function call: {func_call}")
            print(f"Function call type: {type(func_call)}")
            
            if hasattr(func_call, 'arguments'):
                arg = func_call.arguments[0]
                print(f"Argument: {arg}")
                print(f"Argument type: {type(arg)}")
                print(f"Argument repr: {repr(arg)}")
                
                # Check if it's a Descendants
                from jsonpath_ng.jsonpath import Descendants
                print(f"Is Descendants? {isinstance(arg, Descendants)}")
                
                if hasattr(arg, 'left') and hasattr(arg, 'right'):
                    print(f"Left: {arg.left} (type: {type(arg.left)})")
                    print(f"Right: {arg.right} (type: {type(arg.right)})")
    
except Exception as e:
    print(f"Parse error: {e}")
    import traceback
    traceback.print_exc()