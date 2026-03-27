from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, ForeignKey
# from sqlalchemy.orm import Session

engine = create_engine('sqlite:///./alchemy_tutorial/mydatabase2.db', echo=True)
# engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/tutorial_database.db', echo=True)
# Se puede cambiar el motor de la DB. Abstraccion de capas de Alchemy
# echo=True es el verbose para ver que sucede paso a paso

meta = MetaData()

people = Table (
    "people",
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('age', Integer)
)

## TABLE RELATION
# One people -> Many things

things = Table (
    "things",
    meta,
    Column('id', Integer, primary_key=True),
    Column('description', String, nullable=False),
    Column('value', Float),
    Column('owner', Integer, ForeignKey('people.id'))
)

meta.create_all(engine)
conn = engine.connect()

## INSERT DATA with dictionary

insert_people = people.insert().values([
    {'name': 'Jane', 'age': 32},
    {'name': 'Mike', 'age': 30},
    {'name': 'Bob', 'age': 35},
    {'name': 'Anna', 'age': 38},
    {'name': 'John', 'age': 50},
    {'name': 'Clara', 'age': 42}
])

insert_things = things.insert().values([
    {'owner': 2, 'description': 'Laptop', 'value': 800.50},
    {'owner': 2, 'description': 'Mouse', 'value': 50.50},
    {'owner': 2, 'description': 'Keyboard', 'value': 100.50},
    {'owner': 3, 'description': 'Book', 'value': 30},
    {'owner': 4, 'description': 'Bottle', 'value': 10.50},
    {'owner': 3, 'description': 'Speakers', 'value': 80.50}
])

conn.execute(insert_people)
conn.commit()

conn.execute(insert_things)
conn.commit()
