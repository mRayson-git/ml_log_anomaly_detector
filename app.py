import psycopg2

conn = psycopg2.connect(
  host = 172.30.136.222,
  database = "suppliers",
  user = "postgres",
  password = "postgres")
print(conn)
