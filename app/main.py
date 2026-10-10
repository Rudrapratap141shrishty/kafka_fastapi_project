from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session

from .database import Base
from .database import engine
from .database import get_db

from .models import Order
from .schemas import OrderCreate

from .kafka_producer import send_order_event


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Kafka Order API",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "Kafka + FastAPI + PostgreSQL"
    }


@app.post("/orders")
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):

    new_order = Order(

        customer_name=order.customer_name,

        product=order.product,

        quantity=order.quantity,

        price=order.price,

        status="CREATED"
    )

    db.add(new_order)

    db.commit()

    db.refresh(new_order)


    event = {

        "id": new_order.id,

        "customer_name":
            new_order.customer_name,

        "product":
            new_order.product,

        "quantity":
            new_order.quantity,

        "price":
            new_order.price,

        "status":
            new_order.status
    }


    send_order_event(event)


    return {

        "message": "Order created",

        "order": event
    }


@app.get("/orders")
def get_orders(
    db: Session = Depends(get_db)
):

    return db.query(Order).all()