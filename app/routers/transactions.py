
from fastapi import APIRouter,HTTPException,status,Query
from sqlmodel import select
from models import Transaction,CreateTransaction, Customer 
from db import SessionDep

router = APIRouter()


@router.post("/transactions",status_code=status.HTTP_201_CREATED,tags=['transaction'])
async def create_transaction(transaction_data:CreateTransaction,session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer,transaction_data_dict.get('customer_id'))
    if not customer:
        raise HTTPException(status_code=404,detail='we cant find it')
    transaction_db =Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_data


@router.get("/transactions",response_model=list[Transaction],tags=['transaction'])
async def list_transactions(
        session:SessionDep,
        skip: int = Query(0,description ="Registros a omitir"),
        limit: int = Query(10,description = "Numero de registros"),
        ):
    query = select(Transaction).offset(skip).limit(limit)
    response = session.exec(query).all()
    return response