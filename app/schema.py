from pydantic import BaseModel


class OrderCreate(BaseModel):

    customer_name: str

    product: str

    quantity: int

    price: float