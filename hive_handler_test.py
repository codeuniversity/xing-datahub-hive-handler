import hive_handler
import unittest

mock_schema = "foo INT, bar Array<INT>, baz STRING"

class TestSchemaParsing(unittest.TestCase):

  def test_handler(self):
    hive_handler.create_table('test_table', mock_schema)

    arr = hive_handler.fetch('test_table', mock_schema)
    self.assertListEqual(arr, [], msg='Should be empty')

    hive_handler.cursor.execute("INSERT INTO TABLE test_table select 11, Array(1,2), 'bla'")

    hash = hive_handler.fetch('test_table', mock_schema)[0]
    expected_hash = {'foo': 11, 'bar':[1,2], 'baz': 'bla'}
    self.assertDictEqual(hash, expected_hash, msg='Data is not correct')

    hive_handler.drop_table('test_table')


if __name__ == '__main__':
    unittest.main()
