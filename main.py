from fastapi import FastAPI,HTTPException
from models import Customer,Transaction,Invoice,CustomerBase,CreateCustomer



app = FastAPI()

@app.get("/")
async def home():
    return{"Hello":"Juan🤑"}

db_customers: list[Customer]=[]

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data:Customer):
    customer = Customer.model_validate(customer_data.model_dump()) #devuelve un diccionario con los datos
    customer.id = len(db_customers) + 54
    db_customers.append(customer)
    return customer

@app.get("/customers/{customer_id}",response_model = CustomerBase)
async def find_customer(customer_id: int):
    
    for i in db_customers:
        if i.id == customer_id:
           
            return i   
    raise HTTPException(status_code=404, detail="Client not found")
@app.get("/customers")
async def list_customers():
    return db_customers
@app.post("/transactions")
async def create_transaction(transaction_data:Transaction):
    
    return transaction_data
@app.post("/invoices")
async def create_invoices(invoices_data:Invoice):
    
    return invoices_data