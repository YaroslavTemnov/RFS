import psycopg2
from config import load

def connect():
    try:
        params = load()
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Connection error: {error}")
        return None