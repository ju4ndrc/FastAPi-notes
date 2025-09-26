
from fastapi import APIRouter, status, HTTPException, Query
from sqlmodel import select
from models import Customer, CreateCustomer, UpdateCustomer, Plan, CustomerPlan, StatusEnum
from db import SessionDep

router = APIRouter()

@router.post("/customers", response_model=Customer,tags=['customers'])
async def create_customer(customer_data:CreateCustomer, session:SessionDep):
    customer = Customer.model_validate(customer_data.model_dump()) #devuelve un diccionario con los datos
    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer
    # try:
    #     session.add(customer)
    #     session.commit()
    #     session.refresh(customer)
    #     return customer
    # except IntegrityError:
    #     session.rollback()  # Rollback the transaction to keep the session clean
    #     raise HTTPException(
    #         status_code=400,
    #         detail="A customer with this email already exists."
    #     )

# @router.get("/customers/{customer_id}",response_model = CustomerBase)
# async def find_customer(customer_id: int):
    
#     for i in db_customers:
#         if i.id == customer_id:
           
#             return i   
#     raise HTTPException(status_code=404, detail="Client not found")

@router.get("/customers",response_model=list[Customer],tags=['customers'])
async def list_customers(session:SessionDep):
    response = session.exec(select(Customer)).all()
    return response

#con session intentar  un nuevo endpoint que obtenga un customer con un id especifico

@router.get("/customers/{customer_id}",tags=['customers'])
async def find_customer(customer_id: int ,session:SessionDep) -> Customer:

    customer = session.get(Customer, customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="We can not find, this customer")
    return customer
#Extraido de la documentacion FastAPI 👆 https://fastapi.tiangolo.com/tutorial/sql-databases/#read-heroes

@router.delete("/delete_customers/{customer_id}",tags=['customers'])
async def delete_customer(customer_id: int ,session:SessionDep) -> Customer:

    customer = session.get(Customer, customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer doesnt exits")
    session.delete(customer)
    session.commit()
    return {"ok":True}

@router.patch("/update_customer/{id}",response_model=Customer,status_code=status.HTTP_201_CREATED,tags=['customers'])
async def update_customer(customer_id : int, customer_data: UpdateCustomer,session: SessionDep):
    customer_db = session.get(Customer, customer_id)

    if not customer_db:
        raise HTTPException(status_code=404, detail="We can not find, this customer")

    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

#customers?key=valor
@router.post("/customers/{customer_id}/plans/{plan_id}")
async def subscribe_customer_to_plan(customer_id:int, plan_id:int , session:SessionDep , plan_status :StatusEnum = Query()):
    customer_db = session.get( Customer,customer_id )
    plan_db = session.get(Plan, plan_id)

    if not customer_db or not plan_db:
        raise HTTPException(status_code = 404 , detail="We cant find this customer or plan")

    #aqui creamos la relacion entre cusmoter y plan con el id

    customer_plan_db = CustomerPlan(plan_id = plan_db.id, customer_id = customer_db.id)

    customer_plan_db = CustomerPlan(

        plan_id = plan_db.id, customer_id = customer_db.id,
        status = plan_status
    )
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db

@router.get("/customers/{customer_id}/plans/")
async def subscribe_customer_to_plan(customer_id:int,session:SessionDep , plan_status: StatusEnum = Query()):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=404, detail="We cant find this customer ")


    query = (
        select(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_id) #Aqui se filtran todos los CustomerPlan de customer_id
        .where(CustomerPlan.status == plan_status) #Aqui se filtran todos los de estado
         )

    plans = session.exec(query).all() #.exec permite ejecutar una query y .all() obtiene toda la lista

    return plans