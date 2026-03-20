from dotenv import load_dotenv
import os, smtplib

load_dotenv()

sender = os.getenv('EMAIL_USER', '')
password = os.getenv('EMAIL_PASS', '')

# Strip optional quotes
if sender:
    sender = sender.strip().strip('"').strip("\'")
if password:
    password = password.strip().strip('"').strip("\'")

if not sender or not password:
    print('MISSING_CREDENTIALS')
    raise SystemExit(2)

receiver = sender
msg = f"Subject: AssetGuard SMTP Test\n\nTeste de envio automático do AssetGuard.\n"

try:
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as server:
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg)
    print('OK_SENT')
except Exception as e:
    print('ERROR:', type(e).__name__, str(e))
    raise
