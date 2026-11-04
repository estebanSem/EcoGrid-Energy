import os
import requests
from datetime import datetime, timedelta, timezone

TOKEN = "16a3f791c283be6e990fabaf3efc84b6f5027861aa0fa3eb1194ee03ee250644"

# Indicador 1001: Generación por tecnología en tiempo real
INDICATOR_ID = "10211"

# Ventana de tiempo: Últimas 24 horas
now = datetime.now(timezone.utc)
start_date = (now - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
end_date = now.strftime("%Y-%m-%dT23:59:59Z")

url = f"https://api.esios.ree.es/indicators/{INDICATOR_ID}"

headers = {
    "Accept": "application/json; application/vnd.esios-api-v2+json",
    "Content-Type": "application/json",
    "x-api-key": TOKEN,
    "Authorization": f'Token token="{TOKEN}"',
    "User-Agent": "EcoGridDataPipeline/1.0"
}

params = {
    "start_date": start_date,
    "end_date": end_date,
    "time_trunc": "hour"
}

response = requests.get(url, headers=headers, params=params)

print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    indicator = data.get("indicator", {})
    values = indicator.get("values", [])
    
    print("✅ Conexión a eSIOS exitosa!")
    print(f"Indicador: {indicator.get('name')}")
    print(f"Registros recibidos: {len(values)}")
    
    # Muestra los primeros 3 valores recibidos si la lista no está vacía
    if values:
        print("\nEjemplo de datos recibidos:")
        for v in values[:3]:
            print(f" - [{v.get('datetime')}] {v.get('title')}: {v.get('value')} MW")
else:
    print("❌ Error de respuesta:")
    print(response.text)