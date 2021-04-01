import psycopg2
import re

def isOutlier(string):
    if string[0] != '-':
        return 1
    return 0

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
  cur.execute('''CREATE TABLE IF NOT EXISTS log_t (
    log_id serial PRIMARY KEY,
    time varchar(30),
    message varchar(30000),
    lognum varchar(30),
    is_anomalous varchar(30)
    )''')
  
  # Parse File
  limit = 0
  extractedData = []

  mylines = []                             
  with open ('Thunderbird.log', 'rt') as myfile:
    for myline in myfile:
      mylines.append(myline)
    for element in mylines:
      isAnomaly = isOutlier(element)
      match = re.search(r'\d{2}:\d{2}:\d{2}',element)     # getting the time of log
      text = element.split(':')                           # splitting :
      code = element.split('2005')
      arr = []
      arr.append(match.group())
      if(text[-2].strip('') == ' Warning'):
        arr.append(text[-2] + ': ' + text[-1]) 
      else:
        arr.append(text[-1])                                # getting last element after : which is message
      code[0] = code[0].replace('-','')
      arr.append(code[0])
      arr.append(isAnomaly)
      extractedData.append(arr)
      
  #   Now that extracted data has all the logs, we add them to the table
  print('Adding transactions to the database...')
  for log in extractedData:
    cur.execute("INSERT INTO log_t(time, message, lognum, is_anomalous) VALUES (%s, %s, %s, %s)",(log[0], log[1], log[2], log[3]))
  

except (Exception, psycopg2.DatabaseError) as error:
  print(error)

finally:
  if conn is not None:
    conn.commit()
    conn.close()
    print('Database connection closed.')
