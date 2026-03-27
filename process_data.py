from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

EXCEL_FOLDER = Path("relatorios/excel")
CHART_FOLDER = Path("relatorios/graficos")

EXCEL_FOLDER.mkdir(parents=True,exist_ok=True)
CHART_FOLDER.mkdir(parents=True,exist_ok=True)


def load_today_data():
    today = datetime.now().strftime("%Y-%m-%d")
    file = Path("dados/raw") / f"market_snapshot_{today}.csv"

    if not file.exists():
        print("Arquivo do dia não encontrado.")
        return pd.DataFrame(), None

    df = pd.read_csv(file)
    return df, today

def classify_movement(percent_change):
    if pd.isna(percent_change):
        return "Sem dado"
    if percent_change >1 :
        return "Alta forte"
    if percent_change >0:
        return "Alta"
    if percent_change==0:
        return "Estavel"
    if percent_change > - 1:
        return "Queda"
    return "Queda Forte"


def build_highlights (summary):
    top_gainer = summary.sort_values("percent_change", ascending= False).iloc[0]
    top_loser = summary.sort_values("percent_change", ascending= True).iloc[0]
    top_volume = summary.sort_values("volume", ascending=False).iloc[0]

    return{
        "top_gainer": top_gainer,
        "top_loser": top_loser,
        "top_volume":top_volume
    }

def generate_report(df,report_date):
    if df.empty:
        print("Sem dados para processar")
        return None
    #transformacao
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    summary = (df.sort_values("timestamp")
               .groupby("ticker", as_index=False).last())
    summary["movement_class"] = summary["percent_change"].apply(classify_movement)

    top_3 = summary.sort_values("percent_change", ascending=False).head(3)
    volume_ranking = summary.sort_values("volume", ascending=False)

    highlights = build_highlights(summary)

    plt.figure(figsize=(9, 4))
    plt.bar(summary["ticker"], summary["close"])
    plt.title("Último preço por ativo")
    plt.xlabel("Ticker")
    plt.ylabel("Preço de fechamento")
    plt.tight_layout()

    chart_file = CHART_FOLDER /f"chart_{report_date}.png"
    plt.savefig(chart_file, dpi=150)
    plt.close()

    print(f"Gráfico gerado: {chart_file}")


    excel_file = EXCEL_FOLDER / f"report_{report_date}.xlsx"

    with pd.ExcelWriter(excel_file,engine="openpyxl") as writer:
        df.to_excel(writer,sheet_name="dados_brutos",index=False)
        summary.to_excel(writer,sheet_name="resumo", index=False)
        top_3.to_excel(writer,sheet_name="top_3", index = False)
        volume_ranking.to_excel(writer, sheet_name="ranking_volume", index=False)

    print(f"Excel gerado: {excel_file}")

    return{
        "summary": summary,
        "highlights": highlights,
        "chart":chart_file,
        "excel":excel_file

        }