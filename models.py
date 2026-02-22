from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class ProcessedEmail(Base):
    __tablename__ = "processed_emails"
    id = Column(Integer, primary_key=True)
    message_id = Column(String, unique=True)
    sender = Column(String)
    subject = Column(String)
    date_received = Column(DateTime, default=datetime.datetime.utcnow)
