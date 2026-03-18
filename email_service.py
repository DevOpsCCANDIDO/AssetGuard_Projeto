import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Carrega as credenciais do .env
load_dotenv()

def send_inventory_email(action_type, asset_data):
    """
    Implementa a US07: Envio de e-mail em formato HTML após Inserção/Atualização/Deleção.
    """
    # Configurações do remetente (Devem estar no seu .env)
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    receiver_email = "devopsccandido@gmail.com" # Destinatário fixo conforme blueprint

    if not sender_email or not sender_password:
        print("⚠️ Erro: Credenciais de e-mail não configuradas no .env")
        return False

    # Mensagem padronizada conforme blueprint
    subject = f"AssetGuard Alerta: Um registro foi {action_type}"
    
    # Criação do corpo HTML com tabela
    html_content = f"""
    <html>
    <body>
        <h2>Notificação de Alteração de Inventário</h2>
        <p>A seguinte ação foi realizada: <strong>{action_type}</strong></p>
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f2f2f2;">
                <th>Campo</th>
                <th>Valor</th>
            </tr>
            <tr><td>ID</td><td>{asset_data.get('id')}</td></tr>
            <tr><td>Nome do Ativo</td><td>{asset_data.get('asset_name')}</td></tr>
            <tr><td>Tipo</td><td>{asset_data.get('asset_type')}</td></tr>
            <tr><td>Valor</td><td>R$ {asset_data.get('value', 0):.2f}</td></tr>
            <tr><td>Cargo</td><td>{asset_data.get('role')}</td></tr>
            <tr><td>Atribuído a</td><td>{asset_data.get('assigned_to')}</td></tr>
            <tr><td>Regime</td><td>{asset_data.get('regime')}</td></tr>
            <tr><td>Status</td><td>{asset_data.get('status')}</td></tr>
            <tr><td>Tags</td><td>{', '.join(asset_data.get('tags', []))}</td></tr>
            <tr><td>Data Aquisição</td><td>{asset_data.get('acquisition_date')}</td></tr>
            <tr><td>Violação Compliance</td><td>{'Sim' if asset_data.get('compliance_violation') else 'Não'}</td></tr>
        </table>
        <br>
        <p><em>Este é um e-mail automático gerado pelo sistema AssetGuard.</em></p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    try:
        # Configuração para Gmail (padrão comum, pode ser alterado conforme o provedor)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {str(e)}")
        return False