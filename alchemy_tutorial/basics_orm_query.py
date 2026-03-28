from sqlalchemy import create_engine, Integer, String, Float, Column, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///./alchemy_tutorial/mydatabase2.db', echo=True)
# engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/tutorial_database.db', echo=True)
# Se puede cambiar el motor de la DB. Abstraccion de capas de Alchemy
# echo=True es el verbose para ver que sucede paso a paso

Base = declarative_base()

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)

    things = relationship('Thing', back_populates='person')

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

result = session.query(Person.name, Person.age).all()
print (result)

print ("-*-" * 5)

result = session.query(Person).all()
print ([item.name for item in result])

print ("-*-" * 5)
# Prints object mem id unless self representation defined in class declrataion
# def __repr__(self)
result = session.query(Person).all()
print (result)

print (" - - - +" *4)
### QUERY + FILTER
result = session.query(Person.name, Person.age).filter(Person.age > 50).all()
print ([item.name for item in result])
print (" - - - +" *4)
print (result)


