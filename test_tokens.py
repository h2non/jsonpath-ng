#!/usr/bin/env python3

from jsonpath_ng.lexer import JsonPathLexer

# Test what tokens are generated for function call
lexer = JsonPathLexer()
test_string = "match(@.a, 'a.*')"

print("Tokens for function call:")
for token in lexer.tokenize(test_string):
    print(f'{token.type}: {token.value}')