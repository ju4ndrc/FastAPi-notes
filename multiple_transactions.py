from sqlmodel import Session
from db import engine
from models import Customer, Transaction

session = Session(engine)

customer = Customer(
    name = "Juan",
    description = "Student of enginiering",
    email = "juan@sumama.com",
    age = 18,
)

session.add(customer)
session.commit()

for i in range(100):
    session.add(
        Transaction(
            customer_id = customer.id,
            description = f"Test number {i}",
            ammount = 10 * i,
        )
    )
session.commit()