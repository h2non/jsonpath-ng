from jsonpath_ng import parse

jp = parse('$[?value(@.*)==4]')
data = [[4, 4], {'foo': 4, 'bar': 4}]
result = [match.value for match in jp.find(data)]
print(f"Result: {result}")
print(f"Expected: []")