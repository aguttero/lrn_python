from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, ForeignKey
# from sqlalchemy.orm import Session

engine = create_engine('sqlite:///./alchemy_tutorial/mydatabase.db', echo=True)
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

meta.create_all(engine)

# connection
conn = engine.connect()

## INSERT DATA
# insert_statement = people.insert().values(name='Mike', age=30)
# # same insert command with another syntax (adding insert module in from)
# # insert_statement = insert(people).values(name='Jane', age=32)
# result = conn.execute(insert_statement)
# conn.commit()

## SELECT DATA
select_statement = people.select().where(people.c.age >= 30)
# select_statement = people.select() # Selects all
result = conn.execute(select_statement)

for row in result.fetchall():
    print ("row:", row)

# UPDATE DATA
update_statement = people.update().where(people.c.name == 'Mike', people.c.id == 2).values(age=40)
result = conn.execute(update_statement)
conn.commit()

select_statement = people.select() # Selects all
result = conn.execute(select_statement)
for row in result.fetchall():
    print ("updated row:", row)

# DELETE DATA
delete_statement = people.delete().where(people.c.name == 'Mike', people.c.id == 4)
result = conn.execute(delete_statement)
conn.commit()

select_statement = people.select() # Selects all
result = conn.execute(select_statement)
for row in result.fetchall():
    print ("updated row:", row)


