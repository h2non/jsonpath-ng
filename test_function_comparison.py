#!/usr/bin/env python3

from jsonpath_ng import parse

try:
    jp = parse("$[?match(@.a, 'a.*')==true]")
    print('ERROR: Should have failed for function compared to boolean')
except Exception as e:
    print(f'Correctly rejected: {e}')