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

    # passive_deletes="all" evita que SQLAlchemy setee en NULL los hijos en memoria
    # things = relationship('Thing', back_populates='person')
    things = relationship('Thing', back_populates='person', passive_deletes="all")

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Person {self.name}>'

class Thing(Base):
    __tablename__ = 'things'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    value = Column(Float)
    # FK debe llevar nullable = False
    owner = Column(Integer, ForeignKey('people.id'), nullable=False)

    person = relationship ('Person', back_populates='things')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


## RESTRIC DELETE + ERROR HANDLING:
def safe_delete_person (person_id):
    person_to_delete = session.get(Person, person_id) # chose person.id i.e 10
    if not person_to_delete:
        print (f"Error: person_id {person_id} not found")
        return f"Error: person_id {person_id} not found"

    try:
        session.delete(person_to_delete)
        session.commit() # Here the event listener validates
        print ("OK Delete Transaction")

    except IntegrityError as e:
        # Reverts Person and Things update
        session.rollback()
        print (f"Error: Integrity: {e}")
        print(f"Error: person_id {person_id}, {person_to_delete.name} has child objects")

    except Exception as e:
        session.rollback()
        print (f"Error: Unexpected: {e}")

print ("-*-" * 5)

## CODE RUN
result = safe_delete_person(10)

## QUERY
result = session.query(Person.id, Person.name, Person.age).all()
print (result)
print ("-*-" * 5)

result = session.query(Thing.id, Thing.owner, Thing.description, Thing.value).all()
print (result)
print ("-*-" * 5)

print ("//-//-" * 5)
session.close()