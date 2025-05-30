import smtplib
from email.mime.text import MIMEText

def enviar_email_necessidade(itens, destinatario, remetente, senha_app):
    corpo = "Precisamos repor os seguintes itens:\n\n"
    for item, quantidade in itens.items():
        corpo += f"- {item}: {quantidade} unidades\n"
    corpo += "\nPor favor, providenciar o quanto antes."

    msg = MIMEText(corpo)
    msg['Subject'] = 'Reposição de Estoque Necessária'
    msg['From'] = remetente
    msg['To'] = destinatario

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(remetente, senha_app)
            server.send_message(msg)
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
