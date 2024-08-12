# utils/email.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

def enviar_email(destinatario, assunto, mensagem):
    print(destinatario, "destina")
    remetente_email = 'agendamento.coworking@crea-rn.org.br'  # Seu e-mail remetente
    remetente_nome = 'Tarefa '  # Seu nome ou o nome do remetente

    # Configurar o corpo do e-mail
    msg = MIMEMultipart()
    msg['From'] = formataddr((remetente_nome, remetente_email))
    msg['To'] = destinatario
    msg['Subject'] = assunto

    # Adicionar mensagem ao corpo do e-mail
    msg.attach(MIMEText(mensagem, 'plain'))

    # Configurações do servidor SMTP (exemplo com Office 365)
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(remetente_email, 'Crea@2023')  # Substitua com sua senha

    # Enviar e-mail
    text = msg.as_string()
    server.sendmail(remetente_email, destinatario, text)

    # Fechar conexão com o servidor
    server.quit()

    print(f'E-mail enviado para {destinatario} com sucesso.')
