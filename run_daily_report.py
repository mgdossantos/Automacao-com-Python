from process_data import load_today_data,generate_report
from pdf_report import generate_pdf
from send_email import send_email

def main():
    print("Iniciando a geracao de relatorios...\n")
    df,date=load_today_data()

    if df.empty:
        print("Sem dados disponiveis")
        return
    outputs = generate_report(df,date)
    if  not outputs:
        return
    pdf_file = generate_pdf(
        summary = outputs["summary"],
        chart_path = outputs ["chart"],
        highlights = outputs["highlights"],
        report_date = date
    )
    send_email(pdf_file)
if __name__ == "__main__":
    main()