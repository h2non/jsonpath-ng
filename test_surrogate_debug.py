#!/usr/bin/env python3

from jsonpath_ng.lexer import JsonPathLexer

# Test the lexer directly
lexer = JsonPathLexer()

# Test surrogate pair
test_string = r'$["\uD834\uDD1E"]'
print(f"Input string: {test_string}")

try:
    tokens = list(lexer.tokenize(test_string))
    for token in tokens:
        print(f"Token: {token.type} = {repr(token.value)}")
except Exception as e:
    print(f"Error during tokenization: {e}")

# Test invalid surrogate
test_invalid = r'$["\uD800"]'
print(f"\nInvalid test: {test_invalid}")

try:
    tokens = list(lexer.tokenize(test_invalid))
    for token in tokens:
        print(f"Token: {token.type} = {repr(token.value)}")
    print("ERROR: Should have failed!")
except Exception as e:
    print(f"Correctly rejected: {e}")