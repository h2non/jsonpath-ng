#!/usr/bin/env python3

from jsonpath_ng import parse

try:
    jp = parse('$[?length(@.*)<3]')
    print('ERROR: Should have failed for non-singular query @.*')
except Exception as e:
    print(f'Correctly rejected: {e}')