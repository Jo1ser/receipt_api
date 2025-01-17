from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total = Column(Numeric(14, 2), default=0)
    payment_type = Column(String, nullable=True)
    payment_amount = Column(Numeric(14, 2), default=0)
    receipt_link = Column(String, unique=True, nullable=True)

    user = relationship("User")

class ReceiptItem(Base):
    __tablename__ = "receipt_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Numeric(14, 2), default=0)
    quantity = Column(Numeric(14, 3), default=1)
    total = Column(Numeric(14, 2), default=0)
    extra_data = Column(Text, nullable=True)

    receipt = relationship("Receipt", backref="items")
