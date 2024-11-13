from modules.base import Base
from schemas.alert import SchemaAlert
from schemas.payload import SchemaPayload
from schemas.station_parameter import SchemaStationParameter
from schemas.parameter import SchemaParameter
import datetime
import psycopg2
from psycopg2 import sql

class ModuleAlert(Base):
    def get_alerts_by_station_parameter_id(self, station_parmeter_id: int) -> list[SchemaAlert]:
        query: sql.SQL = sql.SQL("SELECT * FROM alertas_alerta WHERE estacao_parametro_id = {}").format(sql.Literal(station_parmeter_id))
        self.postgreSQLConnection.cursor.execute(query)
        alerts: list[SchemaAlert] = []
        for alert in self.postgreSQLConnection.cursor.fetchall():
            alerts.append(SchemaAlert(
                id=alert[0],
                created_at=alert[1],
                modified_at=alert[2],
                name=alert[3],
                condition=alert[4],
                station_parameter_id=alert[5]
            ))
        return alerts

    def get_station_parameter_by_id(self, station_parameter_id: int) -> SchemaStationParameter:
        query: sql.SQL = sql.SQL("SELECT * FROM estacoes_estacao_parametro WHERE id = {}").format(sql.Literal(station_parameter_id))
        self.postgreSQLConnection.cursor.execute(query)
        station_parameter = self.postgreSQLConnection.cursor.fetchone()
        return SchemaStationParameter(
            id=station_parameter[0],
            station_id=station_parameter[1],
            parameter_id=station_parameter[2]
        )

    def get_parameter_by_id(self, parameter_id: int) -> SchemaParameter:
        query: sql.SQL = sql.SQL("SELECT * FROM estacoes_parametro WHERE id = {}").format(sql.Literal(parameter_id))
        self.postgreSQLConnection.cursor.execute(query)
        parameter = self.postgreSQLConnection.cursor.fetchone()
        return SchemaParameter(
            id=parameter[0],
            created_at=parameter[1],
            modified_at=parameter[2],
            active=parameter[3],
            name=parameter[4],
            fator=parameter[5],
            offset=parameter[6],
            json_name=parameter[7],
            description=parameter[8],
            category_id=parameter[9]
        )

    def get_last_meter_id(self, station_parameter_id: int) -> int:
        query: sql.SQL = sql.SQL("SELECT * FROM alertas_medicao WHERE estacao_parametro_id = {} ORDER BY id DESC LIMIT 1").format(sql.Literal(station_parameter_id))
        self.postgreSQLConnection.cursor.execute(query)
        meter = self.postgreSQLConnection.cursor.fetchone()
        if meter is None:
            raise Exception(f"No meter found for station_parameter_id {station_parameter_id}")
        return meter[0]

    def save_alert(self, payload: SchemaPayload, alert: SchemaAlert, meter_id: int) -> None:
        try:
            query: sql.SQL = sql.SQL("INSERT INTO alertas_historicoalerta(criado, modificado, timestamp, timestamp_convertido, alerta_id, medicao_id) VALUES ({}, {}, {}, {}, {}, {})").format(sql.Literal(datetime.datetime.now()), sql.Literal(datetime.datetime.now()), sql.Literal(payload.timestamp), sql.Literal(datetime.datetime.fromtimestamp(payload.timestamp)), sql.Literal(alert.id), sql.Literal(meter_id))
            self.postgreSQLConnection.cursor.execute(query)
            self.postgreSQLConnection.conn.commit()
        except Exception as e:
            print(f"{datetime.datetime.now()} [ModuleAlert] Falha ao inserir o alerta no PostgreSQL: {e}")

    def verify_alerts(self, station_parameter_id: int, payload: SchemaPayload) -> None:
        # Use eval to evaluate the condition
        # The condition must be a string like "> 10"
        try:
            alerts = self.get_alerts_by_station_parameter_id(station_parameter_id)
            for alert in alerts:
                station_parameter = self.get_station_parameter_by_id(station_parameter_id)
                parameter = self.get_parameter_by_id(station_parameter.parameter_id)
                json_name = parameter.json_name
                data = payload.data[json_name]
                if eval(f"{data} {alert.condition}"):
                    meter_id = self.get_last_meter_id(station_parameter_id)
                    self.save_alert(payload, alert, meter_id)
        except Exception as e:
            raise Exception(e)
        