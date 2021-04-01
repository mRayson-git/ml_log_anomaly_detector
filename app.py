import psycopg2

try:
  conn = psycopg2.connect(
    host = "172.30.136.222",
    database = "testdb",
    user = "postgres",
    password = "postgres")

  # Create a cursor
  cur = conn.cursor()

  # execute a statement
  print('PostgreSQL database version:')
  cur.execute('SELECT version()')
  
  # display the PostgreSQL database server version
  db_version = cur.fetchone()
  print(db_version)
  
  #   Create a test table
  print('Creating Table...')
  cur.execute('''CREATE TABLE IF NOT EXISTS accounts (
    user_id serial PRIMARY KEY,
    username varchar(10) UNIQUE NOT NULL
    )''')
  
  # Adding test user to table
  print('Adding test data...')
  cur.execute("INSERT INTO accounts(username) VALUES (%s)", ("Bob_9251",))
  

except (Exception, psycopg2.DatabaseError) as error:
  print(error)

finally:
  if conn is not None:
    conn.commit()
    conn.close()
    print('Database connection closed.')
