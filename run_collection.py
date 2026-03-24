from collect_data import collect_market_data

def main():
    df=collect_market_data()

    if df.empty:
        print("Nenhum dado coletado")
    else:
        print("Coleta finalizada com sucesso")


if __name__ == "__main__":
    main()