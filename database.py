import psycopg2

conn = None

def get_connection():
    global conn
    if conn is None:
        conn = psycopg2.connect(database = "xtdb",
                                host= 'localhost',
                                port = 5432)
    return conn

def get_schema(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM information_schema.columns")
    return cursor.fetchall()
