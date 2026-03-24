from pathlib import Path
from datetime import datetime
import requests
import pandas as pd

from config import API_KEY, SYMBOLS, BASE_URL

# Pasta onde os dados serão salvos
RAW_FOLDER = Path("dados/raw")
RAW_FOLDER.mkdir(parents=True, exist_ok=True)


def get_time_bucket():
    hour = datetime.now().hour

    if hour < 12:
        return "morning"
    elif hour < 16:
        return "afternoon"
    else:
        return "end_of_day"


def collect_market_data():
    registros = []

    for symbol in SYMBOLS:
        params = {
            "symbol": symbol,
            "apikey": API_KEY
        }

        try:
            response = requests.get(BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            print(data)

            if "symbol" in data:
                registro = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "collection_period": get_time_bucket(),
                    "ticker": data.get("symbol"),
                    "name": data.get("name"),
                    "exchange": data.get("exchange"),
                    "currency": data.get("currency"),
                    "close": float(data["close"]) if data.get("close") else None,
                    "previous_close": float(data["previous_close"]) if data.get("previous_close") else None,
                    "change": float(data["change"]) if data.get("change") else None,
                    "percent_change": float(data["percent_change"]) if data.get("percent_change") else None,
                    "volume": float(data["volume"]) if data.get("volume") else None,
                }

                registros.append(registro)
                print(f"Coleta realizada com sucesso: {symbol}")

            else:
                print(f"Erro ao coletar {symbol}: {data}")

        except requests.RequestException as e:
            print(f"Erro de conexão ao coletar {symbol}: {e}")

    df = pd.DataFrame(registros)

    if not df.empty:
        today = datetime.now().strftime("%Y-%m-%d")
        arquivo_saida = RAW_FOLDER / f"market_snapshot_{today}.csv"

        # Append automático (acumula ao longo do dia)
        if arquivo_saida.exists():
            df.to_csv(arquivo_saida, mode="a", header=False, index=False)
        else:
            df.to_csv(arquivo_saida, index=False)

        print(f"\nDados salvos em: {arquivo_saida}")

    return df