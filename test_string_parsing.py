#!/usr/bin/env python3

from jsonpath_ng.lexer import JsonPathLexer

# Test how string literals are tokenized
test = "$[?@.a=='c']"
lexer = JsonPathLexer()

print(f"Parsing: {test}")
tokens = list(lexer.tokenize(test))
for token in tokens:
    print(f"Token: {token.type} = '{token.value}'")