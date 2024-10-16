import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from os import getenv
import datetime

load_dotenv()

HOST=getenv("HOST_POSTGRESQL")
PORT=getenv("PORT_POSTGRESQL")
USER="postgres"
PASSWORD=getenv("PASSWORD_POSTGRESQL")

class PostgreSQLConnection:
    def __init__(self):
        print(f"{datetime.datetime.now()} [PostgreSQLConnection] Abrindo conexão com o PostgreSQL")
        self.connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD
        )
        self.cursor = self.connection.cursor()
    
    def closeConnection(self):
        print(f"{datetime.datetime.now()} [PostgreSQLConnection] Fechando conexão com o PostgreSQL")
        self.cursor.close()
        self.connection.close()
    