import smtplib, ssl

port = 465  # For SSL

def send_mail_SMTP(text, sending_email, sending_password, recieving_email):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sending_email, sending_password)
        server.sendmail(sending_email, recieving_email, text)