from datetime import date, time, datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, DateTime, Boolean, func, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DB_PATH = os.environ.get("DB_PATH", "goats.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)
Base = declarative_base()

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    service_code = Column(String, nullable=False)
    service_label = Column(String, nullable=False)
    appt_date = Column(Date, nullable=False)
    appt_time = Column(Time, nullable=False)
    veteran_police = Column(Boolean, default=False)
    sms_opt_in = Column(Boolean, default=False)
    notes = Column(String)
    price = Column(Float, default=0.0)
    tip = Column(Float, default=0.0)
    currency = Column(String, default="usd")
    status = Column(String, default="Scheduled")
    reminded = Column(Boolean, default=False)
    stripe_session_id = Column(String)
    created_at = Column(DateTime, server_default=func.now())

class InboundSMS(Base):
    __tablename__ = "inbound_sms"
    id = Column(Integer, primary_key=True)
    from_number = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

def init_db():
    Base.metadata.create_all(engine)
    with engine.begin() as conn:
        for stmt in [
            "ALTER TABLE appointments ADD COLUMN sms_opt_in BOOLEAN DEFAULT 0",
            "ALTER TABLE appointments ADD COLUMN tip FLOAT DEFAULT 0.0",
            "ALTER TABLE appointments ADD COLUMN reminded BOOLEAN DEFAULT 0"
        ]:
            try: conn.exec_driver_sql(stmt)
            except Exception: pass
