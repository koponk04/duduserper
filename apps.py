import imaplib
import email
import smtplib
from email.message import EmailMessage
from sqlalchemy.orm import sessionmaker
from models import ProcessedEmail, Base
from config import IMAP_HOST, IMAP_PORT, SMTP_HOST, SMTP_PORT, EMAIL_USER, EMAIL_PASS, DB_URL
from sqlalchemy import create_engine

engine = create_engine(DB_URL, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def fetch_and_forward():
    session = Session()
    # Connect to IMAP
    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")
    status, data = mail.search(None, "UNSEEN")
    for num in data[0].split():
        status, msg_data = mail.fetch(num, "(BODY.PEEK[])")  # fetch without marking as seen
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        message_id = msg.get("Message-ID")

        # Skip if already processed
        if session.query(ProcessedEmail).filter_by(message_id=message_id).first():
            continue

        sender = msg.get("From")
        subject = msg.get("Subject")
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()

        # Resend email
        forward = EmailMessage()
        forward["From"] = EMAIL_USER
        forward["To"] = EMAIL_USER  # or target recipient
        forward["Subject"] = f"[Forwarded] {subject}"
        forward.set_content(f"Original sender: {sender}\n\n{body}")

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(forward)

        # Mark as processed
        session.add(ProcessedEmail(message_id=message_id, sender=sender, subject=subject))
        session.commit()

        # Mark email as seen after successful processing
        mail.store(num, '+FLAGS', '\\Seen')

    session.close()
    mail.logout()
