import time
from http.client import  HTTPException

from typing import Annotated

from fastapi import FastAPI,Request,status

from fastapi.params import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import HTMLResponse

from models import Invoice
from db import init_db
from .routers import customers, transactions,plans
#templates
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

##clever
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(app)
    yield
app = FastAPI(lifespan=lifespan)#se ejecuta al comienxo y al final el lifespan

app.mount("/templates", StaticFiles(directory="app/templates"), name="templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


templates = Jinja2Templates(directory="app/templates")

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

@app.get("/templates",response_class=HTMLResponse)
async def root(request:Request):
    return (templates.TemplateResponse
            (
        "index.html",{"request":request}
    ))


@app.post("/invoices")
async def create_invoices(invoices_data:Invoice):

    return invoices_data