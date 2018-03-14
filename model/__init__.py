import ast

def parse_schema(schema_string):
  splits = schema_string.strip().split(',')
  keys = []
  types = []
  for sp in splits:
    inner_split = sp.strip().split(" ")
    keys.append(inner_split[0])
    types.append(inner_split[1])

  return list(keys), list(types)

def parse_literally(string):
  return ast.literal_eval(string)


def parse_tuple(tuple, schema_string):
  keys, types = parse_schema(schema_string)
  h = {}
  for i, v in enumerate(tuple):
    key = keys[i]
    h[key] = parse_literally(v) if "Array" in types[i] else v
  return h

