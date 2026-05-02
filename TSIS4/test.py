import psycopg2
from connect import connect
from psycopg2.extras import DictCursor

conn = connect()
if conn:
    print("success")
else:
    print("error")

cursor = conn.cursor(cursor_factory=DictCursor)
cursor.execute(""" SELECT * FROM game_sessions""")
result = cursor.fetchall()
for i in result:
    print(i)
conn.commit()
print("success")
conn.close()