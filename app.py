import psycopg2

conn = psycopg2.connect(
  host = "172.30.136.222",
  database = "testdb",
  user = "postgres")
print(conn)
