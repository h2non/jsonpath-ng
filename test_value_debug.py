#!/usr/bin/env python3

from jsonpath_ng import parse

# Debug the value function test more carefully
document = {'c': 'cd', 'values': [{'a': 'ab'}, {'c': 'd'}, {'a': None}]}

print("Document:", document)
print()

# Check what $..c returns
c_selector = '$..c'
c_parsed = parse(c_selector)
c_results = [match.value for match in c_parsed.find(document)]
print(f'$..c returns: {c_results} (length: {len(c_results)})')
print(f'value($..c) should return: UNDEFINED (because multiple values)')
print()

# Check what length(@.a) returns for each element in values array
values = document['values']
length_selector = 'length(@.a)'
length_parsed = parse(length_selector)

print("Debugging length(@.a) for each element in values:")
for i, element in enumerate(values):
    try:
        length_results = [match.value for match in length_parsed.find(element)]
        print(f'Element {i} ({element}): length(@.a) -> {length_results}')
    except Exception as e:
        print(f'Element {i} ({element}): length(@.a) -> Error: {e}')

print()
print("Expected results: [{'c': 'd'}, {'a': None}]")
print("This suggests that elements where length(@.a) equals UNDEFINED should match")
print("But length() of a string should return the string length, not UNDEFINED")