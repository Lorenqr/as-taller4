from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from common.config import settings

from .models import Base, Order, OrderCreate, OrderRead, OrderItem, OrderItemCreate

# Configuración DB
DATABASE_URL = settings.ORDERS_DB_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas
Base.metadata.create_all(bind=engine)


# Inicialización de la app
app = FastAPI(title="Orders Service", version="1.0.0")

# Dependencia de sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoints
@app.get("/health")
def health():
    return {"status": "ok", "service": "orders"}


@app.post("/orders", response_model=OrderRead, status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(user_email="cliente@test.com")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        db_item = OrderItem(order_id=db_order.id, product_id=item.product_id, quantity=item.quantity)
        db.add(db_item)

    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/orders", response_model=list[OrderRead])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@app.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return order
