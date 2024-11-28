from src.modules.base import Base
from src.schemas.alert import SchemaAlert
from src.schemas.payload import SchemaPayload
from src.schemas.station_parameter import SchemaStationParameter
from src.schemas.parameter import SchemaParameter
import datetime
from psycopg2 import sql

class ModuleAlert(Base):
    def get_alerts_by_station_parameter_id(self, station_parmeter_id: int) -> list[SchemaAlert]:
        query: sql.SQL = sql.SQL("SELECT * FROM alertas_alerta WHERE estacao_parametro_id = {}").format(sql.Literal(station_parmeter_id))
        self.postgreSQLConnection.cursor.execute(query)
        alerts: list[SchemaAlert] = []
        for alert in self.postgreSQLConnection.cursor.fetchall():
            alerts.append(SchemaAlert(
                id=alert['id'],
                created_at=alert['criado'],
                modified_at=alert['modificado'],
                name=alert['nome'],
                condition=alert['condicao'],
                station_parameter_id=alert['estacao_parametro_id'],
                active=True
            ))
        return alerts

    def get_station_parameter_by_id(self, station_parameter_id: int) -> SchemaStationParameter:
        query: sql.SQL = sql.SQL("SELECT * FROM estacoes_estacao_parametro WHERE id = {}").format(sql.Literal(station_parameter_id))
        self.postgreSQLConnection.cursor.execute(query)
        station_parameter = self.postgreSQLConnection.cursor.fetchone()
        return SchemaStationParameter(
            id=station_parameter['id'],
            station_id=station_parameter['estacao_id'],
            parameter_id=station_parameter['parametro_id']
        )

    def get_parameter_by_id(self, parameter_id: int) -> SchemaParameter:
        query: sql.SQL = sql.SQL("SELECT * FROM estacoes_parametro WHERE id = {}").format(sql.Literal(parameter_id))
        self.postgreSQLConnection.cursor.execute(query)
        parameter = self.postgreSQLConnection.cursor.fetchone()
        return SchemaParameter(
            id=parameter['id'],
            created_at=parameter['criado'],
            modified_at=parameter['modificado'],
            name=parameter['nome'],
            json_name=parameter['nome_json'],
            active=True,
            fator=parameter['fator'],
            offset=parameter['offset'],
            description=parameter['descricao'],
            category_id=parameter['categoria_id']
        )

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
        alerts = self.get_alerts_by_station_parameter_id(station_parameter_id)
        for alert in alerts:
            station_parameter = self.get_station_parameter_by_id(station_parameter_id)
            parameter = self.get_parameter_by_id(station_parameter.parameter_id)
            json_name = parameter.json_name
            data = payload.data[json_name]
            if eval(f"{data} {alert.condition}"):
                meter_id = self.get_last_meter_id(station_parameter_id)  # Implement this method
                self.save_alert(payload, alert, meter_id)
        