from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, Payment, PaymentCreate, PaymentRead
from typing import List
import os

# Configuración DB (Postgres)
DATABASE_URL = os.getenv("PAYMENTS_DB_URL", "postgresql://user:password@localhost:5432/payments_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Payments Service", version="1.0.0")

# Dependencia de sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok", "service": "payments"}

# Crear un pago
@app.post("/payments/", response_model=PaymentRead, status_code=201)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

# Obtener todos los pagos
@app.get("/payments/", response_model=List[PaymentRead])
def get_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()

# Obtener un pago por ID
@app.get("/payments/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return db_payment
