from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel, Field,Relationship
from enum import Enum
class StatusEnum(str, Enum):
    ACTIVE = 'active'
    INNACTIVE = 'innactive'


class CustomerPlan(SQLModel, table=True):
    id : int = Field(primary_key=True)
    plan_id : int = Field(foreign_key="plan.id")
    customer_id : int = Field(foreign_key="customer.id")#con esto se relaciona a nivel de base de datos los dos modelos
    status : StatusEnum = Field(default=StatusEnum.ACTIVE)
class Plan(SQLModel,table= True):
    
    id: int | None = Field(primary_key=True)
    
    name: str = Field(default=None)

    price: int = Field(default=None)
    
    description : str = Field(default=None)

    customers : list["Customer"] = Relationship(
        back_populates="plans", link_model=CustomerPlan 
    )




class CustomerBase(SQLModel):

    name : str = Field(default=None)
    description: str | None = Field(default=None)
    email : EmailStr = Field(default=None)
    age: int = Field(default=None)

class CreateCustomer(CustomerBase):
    pass

class UpdateCustomer(CustomerBase):
    pass

class Customer(CustomerBase,table=True):
    id:int | None = Field(default=None, primary_key=True)
    transactions:list["Transaction"] = Relationship(back_populates="customer") #Guardar la lista de las transacciones y sirve para mostrarlas
    plans : list[Plan] = Relationship(
        back_populates="customers",link_model=CustomerPlan
    )

class TransactionBase(SQLModel):
    ammount:int = Field(default=None)
    description:str | None = Field(default=None)

class CreateTransaction(TransactionBase):
    customer_id : int = Field(foreign_key="customer.id")

class Transaction(TransactionBase , table=True):
    id : int | None = Field(default=None , primary_key=True)
    customer_id : int = Field(foreign_key="customer.id")
    customer:Customer = Relationship(back_populates="transactions")
    
    

class Invoice(BaseModel):
    id:int
    customer:Customer
    transactions:list [Transaction]
    total : int

    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transactions)