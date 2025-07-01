#!/usr/bin/env python3

from jsonpath_ng.parser import JsonPathParser
from jsonpath_ng.lexer import JsonPathLexer

# Test what happens in parsing specifically
parser = JsonPathParser()
lexer = JsonPathLexer()

test_input = r'$["\uD834\uDD1E"]'
print(f"Input: {test_input}")

# First check lexer tokens
tokens = list(lexer.tokenize(test_input))
print("\nLexer tokens:")
for token in tokens:
    if token.type == 'STRING':
        print(f"  STRING: {repr(token.value)} (codepoints: {[hex(ord(c)) for c in token.value]})")
    else:
        print(f"  {token.type}: {token.value}")

# Now parse
try:
    jp = parser.parse(test_input)
    print(f"\nParsed: {jp}")
    if hasattr(jp, 'fields'):
        print(f"Fields: {jp.fields}")
        for field in jp.fields:
            print(f"  Field: {repr(field)} (codepoints: {[hex(ord(c)) for c in field]})")
except Exception as e:
    print(f"Parse error: {e}")
    import traceback
    traceback.print_exc()