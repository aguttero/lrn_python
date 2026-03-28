from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, ForeignKey, func
# from sqlalchemy.orm import Session

# FOR FK ENFORCEMENT IN SQLlite
from sqlalchemy import event
from sqlalchemy.engine import Engine


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

# insert_people = people.insert().values([
#     {'name': 'Jane', 'age': 32},
#     {'name': 'Mike', 'age': 30},
#     {'name': 'Bob', 'age': 35},
#     {'name': 'Anna', 'age': 38},
#     {'name': 'John', 'age': 50},
#     {'name': 'Clara', 'age': 42}
# ])

# insert_things = things.insert().values([
#     {'owner': 2, 'description': 'Laptop', 'value': 800.50},
#     {'owner': 2, 'description': 'Mouse', 'value': 50.50},
#     {'owner': 2, 'description': 'Keyboard', 'value': 100.50},
#     {'owner': 3, 'description': 'Book', 'value': 30},
#     {'owner': 4, 'description': 'Bottle', 'value': 10.50},
#     {'owner': 6, 'description': 'Speakers', 'value': 80.50}
# ])

# conn.execute(insert_people)
# conn.commit()

# conn.execute(insert_things)
# conn.commit()

## INNER JOIN (Coincidencias de ambas tablas)
join_statement = people.join(things, people.c.id == things.c.owner)
select_statement = people.select().with_only_columns(people.c.name, things.c.description, things.c.value).select_from(join_statement)

result = conn.execute(select_statement)

for row in result.fetchall():
    print ("row:", row)

print ("-*- "*5)

## LEFT OUTER JOIN (Todas las filas de la tabla izquierda)
join_statement = people.outerjoin(things, people.c.id == things.c.owner)
select_statement = people.select().with_only_columns(people.c.name, things.c.description, things.c.value).select_from(join_statement)

result = conn.execute(select_statement)

for row in result.fetchall():
    print ("row:", row)

print ("-*- "*5)

## SUM Function
# import func
group_by_statement = things.select().with_only_columns(things.c.owner, func.sum(things.c.value)).group_by(things.c.owner)
result = conn.execute(group_by_statement)

for row in result.fetchall():
    print ("row:", row)

print ("-*- "*5)
# HAVING a Condition or filter
group_by_statement = things.select().with_only_columns(things.c.owner, func.sum(things.c.value)).group_by(things.c.owner).having(func.sum(things.c.value) > 30)
result = conn.execute(group_by_statement)

for row in result.fetchall():
    print ("row:", row)


