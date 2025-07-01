#!/usr/bin/env python3

from jsonpath_ng.lexer import JsonPathLexer

lexer = JsonPathLexer()

# Test the raw input
test_input = r'$["\uD834\uDD1E"]'
print(f"Raw input: {test_input}")

tokens = list(lexer.tokenize(test_input))
for i, token in enumerate(tokens):
    if token.type == 'STRING':
        print(f"Token {i}: {token.type}")
        print(f"  Raw value: {repr(token.value)}")
        print(f"  Length: {len(token.value)}")
        print(f"  Codepoints: {[hex(ord(c)) for c in token.value]}")
        
        # Check if it's the combined character
        if len(token.value) == 1:
            print(f"  Single character: {token.value}")
            print(f"  Is it 𝄞? {token.value == '𝄞'}")
        else:
            print(f"  Multiple characters - not combined properly")
    else:
        print(f"Token {i}: {token.type} = {token.value}")