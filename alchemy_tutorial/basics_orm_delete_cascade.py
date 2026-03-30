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
    
    # cascade="all, delete-orphan" asegura que al borrar la persona, se borren sus cosas.
    # SQLAlchemy maneja el borrado (no SQLite3)
    things = relationship('Thing', back_populates='person', cascade="all, delete-orphan")

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Person {self.name}>'

class Thing(Base):
    __tablename__ = 'things'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    value = Column(Float)
    owner = Column(Integer, ForeignKey('people.id'))

    person = relationship ('Person', back_populates='things')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

## SESION FLUSH + ERROR HANDLING:
# add person + thing with auto id reference

try:
    person_to_delete = session.get(Person, 10) # chose person.id 14
    if person_to_delete:
        session.delete(person_to_delete)
        session.commit()
        print ("OK Delete Transaction")
    else :
        print ("Error: person.id not found")

except IntegrityError as e:
    # Reverts Person and Things update
    session.rollback()
    print (f"Error: Integrity: {e}")
except Exception as e:
    session.rollback()
    print (f"Error: Unexpected: {e}")

print ("-*-" * 5)

## QUERY

result = session.query(Person.id, Person.name, Person.age).all()
print (result)

print ("-*-" * 5)

result = session.query(Thing.owner, Thing.description, Thing.value).all()
print (result)

print ("-*-" * 5)

# result = session.query(Person).all()
# print ([item.name for item in result])

# print ("-*-" * 5)
# # Prints object mem id unless self representation defined in class declrataion
# # def __repr__(self)
# result = session.query(Person).all()
# print (result)

# print (" - - - +" *4)
# ### QUERY + FILTER
# result = session.query(Person.name, Person.age).filter(Person.age > 50).all()
# print ([item.name for item in result])
# print (" - - - +" *4)
# print (result)


## QUERY + DELETE
# result = session.query(Thing).filter(Thing.value < 50).all()
# print ([f"{item.description}: {item.value}" for item in result])
# print ("-*-" * 5)

# result = session.query(Thing).filter(Thing.value < 50, Thing.id == 7).delete()
# session.commit()

# result = session.query(Thing).filter(Thing.value < 50).all()
# print ([f"{item.description}: {item.value}" for item in result])
# print ("-*-" * 5)


## QUERY + UPDATE
# result = session.query(Person).filter(Person.name == 'Charlie').update({'name': 'Charles'}) 
# session.commit()

# result = session.query(Person.id, Person.name, Person.age).all()
# print (result)
# print ("-*-" * 5)


## QUERY + JOIN
# result = session.query(Person.id, Person.name, Thing.description).join(Thing).all()
# print (result)
# print ("-*-" * 5)

## GROUPING
# need to add func to import
# result = session.query(Thing.owner, func.sum(Thing.value)).group_by(Thing.owner).all()
# print (result)
# print ("-*-" * 5)

# result = session.query(Thing.owner, func.sum(Thing.value)).group_by(Thing.owner).having(func.sum(Thing.value)> 50).all()
# print (result)
# print ("-*-" * 5)


print ("//-//-" * 5)
session.close()