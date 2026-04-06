from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    
# CREATE ENGINE    
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///./alchemy_tutorial/aclhemy_tutorial.db", echo=True)  

# ENGINE METADATA
def show_engine_metadata():

    print ("- - ENGINE METADATA - - " * 2)    
    # 1. Nombre del driver (DBAPI) que SQLAlchemy reporta
    print(f"Driver (DBAPI) en uso: {engine.driver}")

    # 2. Nombre del módulo Python que implementa el DBAPI
    print(f"Módulo DBAPI: {engine.dialect.dbapi.__name__}")

    # 3. Versión del adaptador (binding) de Python
    print(f"Versión del adaptador: {engine.dialect.dbapi.version}")

    # 4. Versión real de la librería SQLite3 instalada en el sistema
    # (Se obtiene ejecutando una consulta SQL directamente)
    with engine.connect() as conn:
        sqlite_version = conn.exec_driver_sql("select sqlite_version()").scalar()
        print(f"Versión de SQLite (C-library): {sqlite_version}")

    print ("- - ENGINE METADATA END - - " * 2)    
# show_engine_metadata()

# EMIT CREATE TABLE
Base.metadata.create_all(engine)

## CREATE OBJECTS and PERSIST:
from sqlalchemy.orm import Session

# with Session(engine) as session:
#     spongebob = User(
#         name="spongebob",
#         fullname="Spongebob Squarepants",
#         addresses=[Address(email_address="spongebob@sqlalchemy.org")],
#     )
#     sandy = User(
#         name="sandy",
#         fullname="Sandy Cheeks",
#         addresses=[
#             Address(email_address="sandy@sqlalchemy.org"),
#             Address(email_address="sandy@squirrelpower.org"),
#         ],
#     )
#     patrick = User(name="patrick", fullname="Patrick Star")
#     session.add_all([spongebob, sandy, patrick])
#     session.commit()

# print ("- - - -")
# if session:
#     print ("session_type:", type(session))
#     print ("session_value:", session)
# print ("- - - -")

# Si abrimos session luego hay que cerrarla
session = Session(engine)
## SIMPLE SELECT
def simple_select():
    from sqlalchemy import select
    stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

    print ("- - - -")
    print ("stmt_value:", stmt)
    print ("- - - -")

    for user in session.scalars(stmt):
        print(user)

def session_select_filter_by():
    from sqlalchemy import select
    sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
    print ("sandy_obj:", sandy)
    print ("- - - -")
    print ("sandy.addresses: ", sandy.addresses)
    print ("- - - -")
    print ("sandy.addresses[1]: ", sandy.addresses[1])


session_select_filter_by()

## SELECT with JOIN

# from sqlalchemy import select
# stmt = (
#     select(Address)
#     .join(Address.user)
#     .where(User.name == "sandy")
#     .where(Address.email_address == "sandy@sqlalchemy.org")
# )
# sandy_address = session.scalars(stmt).one()
# print ("- - - -")
# print("sandy_address: ", sandy_address)
# print ("- - - -")

## UPDATE
# stmt = select(User).where(User.name == "patrick")
# patrick = session.scalars(stmt).one()
# patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))
# sandy_address comes from previous select:
# sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"
# session.commit()

## DELETE 1
# sandy = session.get(User, 2)
# sandy.addresses.remove(sandy_address)
# session.flush()

# DELETE 2
# print ("- - - -")
# stmt = select(User).where(User.name == "patrick")
# patrick = session.scalars(stmt).one()
# print ("patrick user:", patrick)
# print ("patrick.address: ", patrick.addresses)
# print ("- - - -")
# session.delete(patrick)
# session.commit()


print ("- - - -")
session.close()
print ("session.close()")

print ("*THE END*")

# SOME DELETES
# with Session(engine) as session:
#     sandy = session.get(User, 2)
#     sandy.addresses.remove(sandy_address)