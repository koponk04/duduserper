from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, ProcessedEmail
from config import DB_URL
from apps import fetch_and_forward
import threading
import time

app = FastAPI()
engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

admin = Admin(app, engine)
admin.add_view(ModelView(ProcessedEmail))

def email_cron():
    while True:
        fetch_and_forward()
        time.sleep(60)  # run every 1 minute

threading.Thread(target=email_cron, daemon=True).start()
