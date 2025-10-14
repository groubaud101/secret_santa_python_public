import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def ft_read_id_secret_santa(fichier):
    with open(fichier, 'r') as f:
        lines = f.read().splitlines()
        if len(lines) >= 2:
            email = lines[0]
            password = lines[1]
            return email, password
        else:
            raise ValueError("Les identifiants de Secret Santa ne sont pas complets")

def ft_send_mail(subject, content, dest_email, source_email, password):
    message = MIMEMultipart()
    message["From"] = source_email
    message["To"] = dest_email
    message["subject"] = subject
    message.attach(MIMEText(content, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls() # Sécuriser la connexion
            server.login(email, password) # Se connecter au serveur
            server.sendmail(source_email, dest_email, message.as_string()) # envoyer l'e-mail
        print(f"E-mail envoyé avec succès !")        
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")

# lire les infos de connexion
email, password = ft_read_id_secret_santa("secret_santa_mail.txt")

def ft_mail_and_log(mail_santa, lang, nom, target):
    if lang == "EN":
        subject = "OH OH OH ! Merry Christmas !"
        content = f"Hello {nom},\nYour secret Santa target is {target}.\nMerry Christmas!"
    else:
        subject = "OH OH OH ! Joyeux Noël !"
        content = f"Bonjour {nom},\nVotre cible du père Noël secret est {target}.\nJoyeux Noël !"
    print(content)
    with open("logs.txt", 'a') as l:
        print(content, file=l)
        print("", file=l)
        # a décommenter pour envoyer les mails
        # ft_send_mail(subject, content, mail_santa, email, password)