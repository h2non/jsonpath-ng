#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.parser import JsonPathParser

# Test parsing just the function arguments
parser = JsonPathParser()

# Test individual parts
print("Testing individual parts:")

# Test @.a
try:
    result1 = parser.parse("@.a")
    print(f"@.a -> {result1} (type: {type(result1)})")
except Exception as e:
    print(f"@.a failed: {e}")

# Test 'a.*' as a literal
try:
    result2 = parser.parse("'a.*'")
    print(f"'a.*' failed - cannot parse as top-level")
except Exception as e:
    print(f"'a.*' failed: {e}")

# Test just @ 
try:
    result3 = parser.parse("@")
    print(f"@ -> {result3} (type: {type(result3)})")
except Exception as e:
    print(f"@ failed: {e}")

# Now test the full function call
print("\nTesting full function call:")
try:
    result4 = parser.parse("$[?match(@.a, 'a.*')]")
    print(f"Function call -> {result4}")
    
    # Look at the structure
    if hasattr(result4, 'right'):
        print(f"Right side: {result4.right}")
        if hasattr(result4.right, 'expression'):
            expr = result4.right.expression
            print(f"Expression: {expr} (type: {type(expr)})")
            if hasattr(expr, 'arguments'):
                print(f"Arguments: {expr.arguments}")
except Exception as e:
    print(f"Function call failed: {e}")
    import traceback
    traceback.print_exc()