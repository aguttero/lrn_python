from sqlalchemy import create_engine, Integer, String, Float, Column, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# FOR FK ENFORCEMENT IN SQLlite
from sqlalchemy import event
from sqlalchemy.engine import Engine

# FOR INTEGRITY ERROR HANDLING
from sqlalchemy.exc import IntegrityError


engine = create_engine('sqlite:///./alchemy_tutorial/mydatabase2.db', echo=True)
# engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/tutorial_database.db', echo=True)
# Se puede cambiar el motor de la DB. Abstraccion de capas de Alchemy
# echo=True es el verbose para ver que sucede paso a paso

# ENABLE FK ENFORCEMENT
# Needs to be placed after engine creation
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

###
Base = declarative_base()

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)

    things = relationship('Thing', back_populates='person')

class Thing(Base):
    __tablename__ = 'things'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    value = Column(Float)
    owner = Column(Integer, ForeignKey('people.id'), nullable=False)

    person = relationship ('Person', back_populates='things')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


## INSERT

# new_person = Person (name='Charlie', age=70)
# session.add(new_person)

## SESION FLUSH + ERROR HANDLING:
# add person + thing with auto id reference
# try:
#     new_person = Person (name='Mike', age=70)
#     session.add(new_person)

#     # FLUSH to obtain the person id
#     session.flush()
    
#     new_thing = Thing(description='Pen', value=3.90, owner=new_person.id) # Owner ID inexistente
#     session.add(new_thing)

#     session.commit()
#     print ("OK Transaction")

# except IntegrityError as e:
#     # Reverts Person and Things update
#     session.rollback()
#     print (f"Error: Integrity: {e}")
# except Exception as e:
#     session.rollback()
#     print (f"Error: Unexpected: {e}")


## INTEGRITY ERROR HANDLING
# from sqlalchemy.exc import IntegrityError

# try:
#     new_thing = Thing(description='Mouse Pad', value=9.90, owner=new_person.id)
#     new_thing = Thing(description='Mouse Pad', value=9.90, owner=999) # Owner ID inexistente
#     session.add(new_thing)
#     session.commit()
# except IntegrityError as e:
#     session.rollback()
#     print(f"Integrity Error Summary: {e.orig}")
#     print(f"Full Error Message: \n{e}")

## Relationship dot notation
# print ("new_thing.person.name: ", new_thing.person.name)
print ("- - +" *5)
# List comprehension
# print ([item.description for item in new_person.things ])


## UPDATE
# Update using the PK
# 1. Buscamos el registro (por ejemplo, por ID)
usuario = session.get(Person, 5)

if usuario:
    # 2. Modificamos el atributo directamente
    usuario.name = "new_name"
    
    # 3. Guardamos los cambios
    session.commit()

print ("- - +" *5)

## UPDATE Masivo - Multiple records
# import 'update'
from sqlalchemy import update

# Actualiza a todos los usuarios que tengan el nombre 'new_name'
# no carga los valores en memoria
stmt = (
    update(Person)
    .where(Person.name == 'new_name')
    .values(name="New_Name")
)

session.execute(stmt)
session.commit()

## UPDATE con diccionario 
# use setttr

datos_nuevos = {"name": "new_name", "age": 55}
usuario = session.get(Person, 4) # Update user with PK id == 4

for clave, valor in datos_nuevos.items():
    setattr(usuario, clave, valor)

session.commit()




session.close()

