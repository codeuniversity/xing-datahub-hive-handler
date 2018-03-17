import model
import unittest

def mock_data():
  mock_schema = "foo INT, bar Array<INT>, baz STRING"
  mock_tuple = (12, '[1,2,3,4]', 'Bla')
  return (mock_tuple, mock_schema)

class TestSchemaParsing(unittest.TestCase):

  def test_parse_schema(self):
    _, schema = mock_data()
    keys, types = model.parse_schema(schema)
    self.assertListEqual(keys, ['foo', 'bar', 'baz'], msg='Parse Schema does not parse the types correctly')
    self.assertListEqual(types, ['INT', 'Array<INT>', 'STRING'], msg='Parse Schema does not parse the types correctly')

  def test_parse_parse_literally(self):
    arr = model.parse_literally('[10,11]')
    self.assertListEqual(arr, [10,11],msg='Parse Literally does not parse array strings correctly')

  def test_parse_tuple(self):
    tuple, schema = mock_data()
    hash = model.parse_tuple(tuple, schema)
    expected_dict = {'foo': 12, 'bar':[1,2,3,4], 'baz': 'Bla'}
    self.assertDictEqual(hash,expected_dict, msg='Parse Tuple does not return the correct dict' )


if __name__ == '__main__':
    unittest.main()
