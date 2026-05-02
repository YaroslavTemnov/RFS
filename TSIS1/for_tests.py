import psycopg2
from psycopg2.extras import DictCursor

def a():
    return "something"



try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        user = "postgres",
        password = "12345678",
        port = 5432,
        dbname = "phonebook"
    )
    print("Connection succesful!")
except:
    print("Conection failed")

cursor = conn.cursor(cursor_factory=DictCursor)    

sql = f"""
    SELECT * FROM groups
    """
cursor.execute(sql)
result = cursor.fetchall()
for res in result:
    print(res)
    
conn.commit()
print("Success")

conn.close()
