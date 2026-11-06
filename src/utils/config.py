from pathlib import Path
import yaml

# 1. Obtener la ruta raíz del proyecto dinámicamente
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.yml"


def load_indicators_config(path: Path = CONFIG_PATH) -> dict:
  """Carga la configuración YAML desde la raíz del proyecto."""
  if not path.exists():
    raise FileNotFoundError(
        f"❌ No se encontró el archivo de configuración en la ruta esperada:"
        f" {path}"
    )

  with open(path, "r", encoding="utf-8") as f:
    return yaml.safe_load(f)

def get_kafka_config(path: Path = CONFIG_PATH) -> dict:
  """Devuelve la configuracion de Kafka

    Args:
        path (Path, optional): ruta del archivo de config. Defaults to CONFIG_PATH.

    Returns:
        dict: _description_
  """
  config = load_indicators_config(path)
  list = config.get("kafka", [])

  return list


def get_indicators_map(path: Path = CONFIG_PATH) -> dict:
  """Devuelve un diccionario donde la clave es el ID del indicador (int)

  para búsqueda rápida (O(1)) durante la ingesta.
  """
  config = load_indicators_config(path)
  gen_list = config.get("esios", {}).get("generation", [])
  return {item["id"]: item for item in gen_list}


