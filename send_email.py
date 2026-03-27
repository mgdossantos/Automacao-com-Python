import smtplib
from email.message import EmailMessage

from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER


def send_email(file_path):
    # criar mensagem
    msg = EmailMessage()
    msg["Subject"] = "Relatório de Mercado"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    msg.set_content(
        "Olá,\n\nSegue em anexo o relatório gerado automaticamente.\n"
    )

    # anexar arquivo (PDF)
    with open(file_path, "rb") as f:
        file_data = f.read()
        file_name = file_path.name

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="pdf",
        filename=file_name
    )

    # conectar ao servidor e enviar
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()  # segurança
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("Email enviado com sucesso!")

    except Exception as e:
        print(f"Erro ao enviar email: {e}")