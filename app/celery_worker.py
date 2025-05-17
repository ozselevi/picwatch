from celery import Celery
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from database import Base, engine, SessionLocal

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
)

@celery_app.task
def send_past_images_to_user(email):
    logger.info(f"Email küldés elindult {email} címre (múltbeli képek)")

    db = SessionLocal()
    images = db.query(ImageModel).all()

    if not images:
        logger.warning("Nincs kép az adatbázisban.")
        db.close()
        return

    message = "Eddigi képek:\n\n"
    for img in images:
        message += f"- {img.description} | Arcok száma: {img.people_detected}\n"

    logger.info(f"{len(images)} kép lekérve, email küldése folyamatban...")
    send_email_notification.delay(email, "Eddigi képek összefoglalója", message)
    db.close()

@celery_app.task
def send_email_notification(to_email, subject, body):
    import smtplib
    from email.mime.text import MIMEText

    logger.info(f"Email küldése: {to_email} | Tárgy: {subject}")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "noreply@yourdomain.com"
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("ozsel01@gmail.com", "faetdhkwtmxaazrd")
            server.send_message(msg)
        logger.info("Email sikeresen elküldve.")
    except Exception as e:
        logger.error(f"Hiba történt email küldés közben: {e}")
