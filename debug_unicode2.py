#!/usr/bin/env python3

from jsonpath_ng import parse

# Test the actual surrogate pair cases from the compliance tests
test_doc_1 = {'𝄞': 'A'}
print(f"Document key: {repr('𝄞')}")
print(f"Document key codepoints: {[hex(ord(c)) for c in '𝄞']}")

jp1 = parse('$["\uD834\uDD1E"]')
print(f"Parsed field: {repr(jp1)}")

# Check what Fields object contains
if hasattr(jp1, 'fields'):
    parsed_key = jp1.fields[0]
    print(f"Parsed key: {repr(parsed_key)}")
    print(f"Parsed key codepoints: {[hex(ord(c)) for c in parsed_key]}")
    print(f"Keys equal? {parsed_key == '𝄞'}")

result1 = jp1.find(test_doc_1)
print(f"Result: {result1}")

# Let's also check the lexer output directly
from jsonpath_ng.lexer import JsonPathLexer
lexer = JsonPathLexer()
tokens = list(lexer.tokenize('$["\uD834\uDD1E"]'))
string_token = [t for t in tokens if t.type == 'STRING'][0]
print(f"String token value: {repr(string_token.value)}")
print(f"String token codepoints: {[hex(ord(c)) for c in string_token.value]}")