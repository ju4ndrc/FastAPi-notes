from fastapi import FastAPI,HTTPException
from models import Customer,Transaction,Invoice,CustomerBase,CreateCustomer
from db import SessionDep,create_all_tables
from sqlmodel import select

app = FastAPI(lifespan=create_all_tables)#se ejecuta al comienxo y al final el lifespan

@app.get("/")
async def home():
    return{"Hello":"Juan🤑"}

db_customers: list[Customer]=[]

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data:CreateCustomer, session:SessionDep):
    customer = Customer.model_validate(customer_data.model_dump()) #devuelve un diccionario con los datos
    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer

# @app.get("/customers/{customer_id}",response_model = CustomerBase)
# async def find_customer(customer_id: int):
    
#     for i in db_customers:
#         if i.id == customer_id:
           
#             return i   
#     raise HTTPException(status_code=404, detail="Client not found")

@app.get("/customers",response_model=list[Customer])
async def list_customers(session:SessionDep):
    response = session.exec(select(Customer)).all()
    return response

#con session intentar  un nuevo endpoint que obtenga un customer con un id especifico

@app.get("/customers/{customer_id}")
async def find_customer(customer_id: int ,session:SessionDep) -> Customer:

    customer = session.get(Customer, customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="We can not find, this customer")
    return customer
#Extraido de la documentacion FastAPI 👆 https://fastapi.tiangolo.com/tutorial/sql-databases/#read-heroes

@app.post("/transactions")
async def create_transaction(transaction_data:Transaction):
    
    return transaction_data
@app.post("/invoices")
async def create_invoices(invoices_data:Invoice):
    
    return invoices_data