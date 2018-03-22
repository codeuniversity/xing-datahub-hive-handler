from pyhive import hive
import model
cursor = hive.connect('localhost').cursor()

user_schema_string = """
  id INT,
  jobroles Array<INT>,
  career_level INT,
  discipline_id INT,
  industry_id INT,
  country STRING,
  region int,
  experience_n_entries_class INT,
  experience_years_experience INT,
  experience_years_in_current INT,
  edu_degree INT,
  edu_fieldofstudies Array<INT>,
  wtcj INT,
  premium INT
  """


item_schema_string = """
  id INT,
  title INT,
  career_level INT,
  discipline_id INT,
  industry_id INT,
  country STRING,
  is_payed INT,
  region INT,
  latitude FLOAT,
  longitude FLOAT,
  employment INT,
  tags Array<int>,
  created_at INT
  """

interaction_schema_string = """
  user_id INT,
  item_id INT,
  interaction_type INT,
  created_at INT
  """

target_user_schema_string = """
  user_id INT
"""

target_item_schema_string = """
  item_id INT
"""

def create_csv_table(name, location, schema_string):
    create_table = """
      CREATE EXTERNAL TABLE {}
      ({})
      ROW FORMAT DELIMITED FIELDS TERMINATED BY ';'
      collection items terminated by '|'
      STORED AS TEXTFILE
      LOCATION '{}'
      """\
        .format(name, schema_string, location)
    print('creating csv table: ', name, '...')
    cursor.execute(create_table)
    print('...done!')

def create_table(name, schema_string):
  query = """
  CREATE TABLE IF NOT EXISTS {}
  ({}) STORED AS ORC
  """.format(name, schema_string)
  cursor.execute(query)

def init():
  create_table('target_items', target_item_schema_string)
  create_table('target_users', target_user_schema_string)
  create_table('interactions', interaction_schema_string)
  create_table('items', item_schema_string)
  create_table('users', user_schema_string)


def insert_from_table(into_table_name, from_table_name):
    insert = "INSERT INTO {} SELECT * from {}".format(into_table_name,from_table_name)
    print('inserting ', into_table_name,' from csv: ', from_table_name)
    cursor.execute(insert)
    print('...done!')


def drop_table(name):
    q = "DROP TABLE {}".format(name)
    print('dropping ', name, '...')
    cursor.execute(q)
    print('...done!')


def fetch(name, schema_string, limit=100, where="True"):
  q = "SELECT * from {} where {} limit {}".format(name, where, limit)
  cursor.execute(q)
  rows = cursor.fetchall()
  l = list(map(lambda row: model.parse_tuple(row, schema_string),rows))
  return l

def fetch_users(limit=100, where="True"):
  return fetch("users", user_schema_string, limit, where)

def fetch_items(limit=100, where="True"):
  return fetch("items", item_schema_string, limit, where)

def fetch_interactions(limit=100, where="True"):
  return fetch("interactions", interaction_schema_string, limit, where)

def fetch_target_users(limit=100, where="True"):
  return fetch("target_users", target_user_schema_string, limit, where)

def fetch_target_items(limit=100, where="True"):
  return fetch("target_items", target_item_schema_string, limit, where)
