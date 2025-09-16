from fastapi import FastAPI
from models import Transaction,Invoice
from db import SessionDep,create_all_tables
from sqlmodel import select
from .routers import customers

app = FastAPI(lifespan=create_all_tables)#se ejecuta al comienxo y al final el lifespan

app.include_router(customers.router)

@app.get("/")
async def home():
    return{"Hello":"Juan🤑"}


@app.post("/transactions")
async def create_transaction(transaction_data:Transaction):
    
    return transaction_data
@app.post("/invoices")
async def create_invoices(invoices_data:Invoice):
    
    return invoices_data