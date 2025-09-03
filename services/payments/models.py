from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

# Modelo SQLAlchemy (tabla en DB)
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, index=True)  # ID de la orden asociada
    amount = Column(Float, nullable=False)  # Monto del pago
    status = Column(String, default="pending")  # pending, completed, failed
    method = Column(String, default="card")  # card, paypal, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Payment(id={self.id}, order_id={self.order_id}, status='{self.status}')>"

# -------- Pydantic Schemas --------
class PaymentBase(BaseModel):
    order_id: int
    amount: float
    method: str

class PaymentCreate(PaymentBase):
    pass

class PaymentRead(PaymentBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


