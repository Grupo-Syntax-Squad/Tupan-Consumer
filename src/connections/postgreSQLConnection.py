import psycopg2
from dotenv import load_dotenv
from os import getenv
import datetime

load_dotenv()

HOST=getenv("HOST_POSTGRESQL")
PORT=getenv("PORT_POSTGRESQL")
USER=getenv("USER_POSTGRESQL")
PASSWORD=getenv("PASSWORD_POSTGRESQL")
DB_NAME=getenv("DB_POSTGRESQL")

class PostgreSQLConnection:
    def __init__(self):
        print(f"{datetime.datetime.now()} [PostgreSQLConnection] Abrindo conexão com o PostgreSQL")
        self.conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        self.cursor = self.conn.cursor()
    
    def close(self):
        print(f"{datetime.datetime.now()} [PostgreSQLConnection] Fechando conexão com o PostgreSQL")
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    import psycopg2
    from os import getenv
    from dotenv import load_dotenv

    load_dotenv()

    HOST = getenv("HOST_POSTGRESQL")
    PORT = getenv("PORT_POSTGRESQL")
    USER = getenv("USER_POSTGRESQL")
    PASSWORD = getenv("PASSWORD_POSTGRESQL")
    DB_NAME = getenv("DB_POSTGRESQL")

    try:
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            dbname=DB_NAME
        )
        print("Connection successful")
    except Exception as e:
        print(f"Connection failed: {e}")