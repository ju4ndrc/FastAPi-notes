import time
from http.client import responses, HTTPException

from typing import Annotated

from fastapi import FastAPI,Request,status

from fastapi.params import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from models import Transaction,Invoice
from db import SessionDep,create_all_tables
from sqlmodel import select
from .routers import customers, transactions,plans

app = FastAPI(lifespan=create_all_tables)#se ejecuta al comienxo y al final el lifespan

app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router , tags=["Plans"], prefix="/Plans")

@app.middleware("http")
async def log_request_time(requets:Request,call_next):
    stat_time = time.time()

    response = await call_next(requets) #aqui se define un middleware basico

    process_time = time.time() - stat_time #aqui se calcula cuamto tardo en ejecutarse response = await call_next(requets)

    print(f"Request: {requets.url} completed in : {process_time:.4f} seconds")

    return response # se retorna una respuesta por que se esta interceptando un request

@app.middleware("http")
async def get_headers(requets: Request, call_next):
    print("Requests Headers")
    for header , value in requets.headers.items():
        print(f"{header}:{value}")
    response = await call_next(requets)
    return response

security = HTTPBasic()
@app.get("/")
async def home(credentials:Annotated[HTTPBasicCredentials, Depends(security)]):
    print(credentials)
    if credentials.username == "lupekoko" and credentials.password == "123":
        return{"Hello":f"{credentials.username}"}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)



@app.post("/invoices")
async def create_invoices(invoices_data:Invoice):
    
    return invoices_data