#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.jsonpath import DatumInContext

# Test slice existence behavior more deeply
document = [1, [], [2], [2, 3, 4], {}, {'a': 3}]

slice_expr = '@[0:2]'
slice_parsed = parse(slice_expr)

print(f'Debugging filter evaluation for each element:')
for i, element in enumerate(document):
    element_datum = DatumInContext(element)
    slice_results = slice_parsed.find(element_datum)
    print(f'Element {i} ({element}):')
    print(f'  @[0:2] returns {len(slice_results)} matches: {[r.value for r in slice_results]}')
    print(f'  Filter evaluation: {len(slice_results) > 0}')
    print()