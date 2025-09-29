import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel,Session
from app.main import  app
from db import get_session

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"


engine = create_engine(
    sqlite_url,
    connect_args = {"check_same_thread" : False  },#se evita que se ejecute codigo en el thread
    poolclass = StaticPool,
)
# poolclass crea la base de datso temporal y en memorua StaticPool

#que hace una fixure? = nos devuelve lo  que retorne con yield
@pytest.fixture(name = "session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine) #dropall permite borrar las tablas para cada prueba

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session #aqui devolvemos la sesion

    app.dependency_overrides[get_session] = get_session_override #aqui nos aseeguramos de usar la session de test
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()