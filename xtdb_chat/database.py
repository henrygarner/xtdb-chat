import psycopg2
import os

conn = None

def get_connection():
    global conn
    if conn is None:
        conn = psycopg2.connect(database = "xtdb",
                                host = os.environ.get('DBHOST', 'localhost'),
                                port = 5432)
    return conn

def get_schema(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM information_schema.columns")
    return cursor.fetchall()
