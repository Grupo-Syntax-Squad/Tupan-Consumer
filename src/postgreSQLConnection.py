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
DB_NAME="tupan"

class PostgreSQLConnection:
    def __init__(self):
        print(f"{datetime.datetime.now()} [PostgreSQLConnection] Abrindo conexão com o PostgreSQL")
        self.connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        self.cursor = self.connection.cursor()
    
    def closeConnection(self):
        print(f"{datetime.datetime.now()} [PostgreSQLConnection] Fechando conexão com o PostgreSQL")
        self.cursor.close()
        self.connection.close()
    
    def getMacAddress(self, mac_address):
        query = sql.SQL("SELECT * FROM estacoes_estacao WHERE topico = {}").format(sql.Literal(mac_address))
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def getEstacaoParametros(self, estacao_id):
        parametros = []
        query = sql.SQL("SELECT * FROM estacoes_estacao_parametro WHERE estacao_id = {}").format(sql.Literal(estacao_id))
        self.cursor.execute(query)
        estacao_parametros = self.cursor.fetchall()
        for estacao_parametro in estacao_parametros:
            query = sql.SQL("SELECT * FROM estacoes_parametro WHERE id = {}").format(sql.Literal(estacao_parametro[2]))
            self.cursor.execute(query)
            parametro = self.cursor.fetchall()[0]
            parametros.append(parametro)
        return estacao_parametros, parametros
    
    def setMedicao(self, timestamp, timestamp_convertido, dados, estacao_parametro_id):
        now = datetime.datetime.now()
        try:
            query = sql.SQL("INSERT INTO alertas_medicao (timestamp, timestamp_convertido, dados, estacao_parametro_id, criado, modificado) VALUES ({}, {}, {}, {}, {}, {})").format(sql.Literal(timestamp), sql.Literal(timestamp_convertido), sql.Literal(dados), sql.Literal(estacao_parametro_id), sql.Literal(now), sql.Literal(now))
            self.cursor.execute(query)
            self.connection.commit()
            print(f"{datetime.datetime.now()} [PostgreSQLConnection] Medição inserida no PostgreSQL")
            return True
        except Exception as e:
            print(f"{datetime.datetime.now()} [PostgreSQLConnection] Falha ao inserir a medição no PostgreSQL: {e}")
            return False