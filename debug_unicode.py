#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.lexer import JsonPathLexer

# Debug surrogate pair parsing
lexer = JsonPathLexer()

# Test what the lexer produces for the surrogate pair
tokens = list(lexer.tokenize('$["\uD834\uDD1E"]'))
print("Tokens for surrogate pair:")
for token in tokens:
    print(f"  {token.type}: {repr(token.value)}")

# Now test parsing 
jp = parse('$["\uD834\uDD1E"]')
print(f"\nParsed JSONPath: {jp}")

# Test what happens when we look for the key
test_doc = {'𝄞': 'A'}
print(f"\nDocument keys: {[repr(k) for k in test_doc.keys()]}")

# Check if the parsed string matches the document key
if hasattr(jp, 'fields'):
    print(f"Looking for field: {repr(jp.fields[0])}")

matches = jp.find(test_doc)
print(f"Matches: {matches}")

# Compare the characters
surrogate_char = '\uD834\uDD1E'  # This should become 𝄞
doc_key = '𝄞'
print(f"\nSurrogate string: {repr(surrogate_char)}")
print(f"Doc key: {repr(doc_key)}")
print(f"Are they equal? {surrogate_char == doc_key}")
print(f"Surrogate ord: {[ord(c) for c in surrogate_char]}")
print(f"Doc key ord: {[ord(c) for c in doc_key]}")