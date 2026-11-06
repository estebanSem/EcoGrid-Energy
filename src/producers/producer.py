from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
from src.utils.config import get_kafka_config
import requests

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

_config = get_kafka_config()
# ruta del fichero esquema-avro
_schema_avro_path = _schema_path = Path(__file__).parent.parent / "schemas" / "energy_event.avsc"

TOKEN_ESIOS     = os.getenv('TOKEN_ESIOS')
KAFKA_BROKER    = _config["bootstrap_server"]
SCHEMA_REGISTRY = _config["schema_registry"]

#TODO --> Crear el schema AVRO
schema_avro = avro.load(_schema_avro_path)

def producer_config(broker: str = KAFKA_BROKER, schema_path: str = SCHEMA_REGISTRY) -> dict :
    return {
        'bootsrap.servers' : broker,
        'schema.registry.url' : schema_path
    }

def create_producer() -> AvroProducer:
    """Crea el productor de Avro

    Returns:
        AvroProducer: _description_
    """
    return AvroProducer(
        config=producer_config,
        default_value_schema=schema_avro
    )

def fetch_esios_indicator(indicator_id: int) -> dict:

    now = datetime.now(timezone.utc)
    start_date = (now - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
    end_date = now.strftime("%Y-%m-%dT23:59:59Z")

    url = f"https://api.esios.ree.es/indicators/{indicator_id}"
    headers = {
        "Accept": "application/json; application/vnd.esios-api-v2+json",
        "Content-Type": "application/json",
        "x-api-key": TOKEN_ESIOS,
        "Authorization": f'Token token="{TOKEN_ESIOS}"',
        "User-Agent": "EcoGridDataPipeline/1.0",
    }
    params = {"start_date": start_date, "end_date": end_date, "time_trunc": "hour"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error al consultar el indicador {indicator_id}: {e}")
        return {}

if __name__ == "__main__":

    res = fetch_esios_indicator(506)

    print(res)

