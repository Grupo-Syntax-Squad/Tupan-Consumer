from schemas.parameter import SchemaParameter
from schemas.station_parameter import SchemaStationParameter
from schemas.station import SchemaStation
from schemas.meter import SchemaMeter
from .base import Base
import datetime
from psycopg2 import sql

class ModuleStation(Base):
    def get_station_by_mac_address(self, mac_address: str) -> list[SchemaStation]:
        query: sql.SQL = sql.SQL("SELECT * FROM estacoes_estacao WHERE topico = {}").format(sql.Literal(mac_address))
        self.postgreSQLConnection.cursor.execute(query)
        stations_schemas: list[SchemaStation] = []
        for station in self.postgreSQLConnection.cursor.fetchall():
            schema = SchemaStation(
                id=station[0],
                created_at=station[1],
                modified_at=station[2],
                active=station[3],
                name=station[4],
                topic=station[5],
                address_id=station[6]
            )
            stations_schemas.append(schema)
        return stations_schemas

    def set_meter(self, timestamp: float, converted_timestamp: datetime, data: any, station_parameter_id: int) -> bool:
        now: any = datetime.datetime.now()
        try:
            query: sql.SQL = sql.SQL("INSERT INTO alertas_medicao(criado, modificado, timestamp, timestamp_convertido, estacao_parametro_id, dados) VALUES ({}, {}, {}, {}, {}, {}) RETURNING id").format(sql.Literal(now), sql.Literal(now), sql.Literal(timestamp), sql.Literal(converted_timestamp), sql.Literal(station_parameter_id), sql.Literal(data))
            self.postgreSQLConnection.cursor.execute(query)
            self.postgreSQLConnection.conn.commit()
            meter_id = self.postgreSQLConnection.cursor.fetchone()[0]
            return SchemaMeter(
                id=meter_id,
                created_at=now,
                modified_at=now,
                timestamp=timestamp,
                converted_timestamp=converted_timestamp,
                station_parameter_id=station_parameter_id,
                data=data
            )
            
        except Exception as e:
            print(f"{datetime.datetime.now()} [PostgreSQLConnection] Falha ao inserir a medição no PostgreSQL: {e}")
            raise Exception(e)
            return False

    def get_station_parameters(self, station_id: int) -> tuple[list[SchemaStationParameter], list[SchemaParameter]]:
        station_parameters: list[SchemaStationParameter] = []
        parameters: list[SchemaParameter] = []
        
        query: sql.SQL = sql.SQL("SELECT * FROM estacoes_estacao_parametro WHERE estacao_id = {}").format(sql.Literal(station_id))
        self.postgreSQLConnection.cursor.execute(query)
        station_parameters_data = self.postgreSQLConnection.cursor.fetchall()
        
        for station_parameter_data in station_parameters_data:
            station_parameter = SchemaStationParameter(
                id=station_parameter_data[0],
                station_id=station_parameter_data[1],
                parameter_id=station_parameter_data[2]
            )
            station_parameters.append(station_parameter)
            
            query = sql.SQL("SELECT * FROM estacoes_parametro WHERE id = {}").format(sql.Literal(station_parameter.parameter_id))
            self.postgreSQLConnection.cursor.execute(query)
            parameter_data = self.postgreSQLConnection.cursor.fetchall()[0]
            
            parameter = SchemaParameter(
                id=parameter_data[0],
                created_at=parameter_data[1],
                modified_at=parameter_data[2],
                active=parameter_data[3],
                name=parameter_data[4],
                fator=parameter_data[5],
                offset=parameter_data[6],
                json_name=parameter_data[7],
                description=parameter_data[8],
                category_id=parameter_data[9]
            )
            parameters.append(parameter)
        
        return station_parameters, parameters