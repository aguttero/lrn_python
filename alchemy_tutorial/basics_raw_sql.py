from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///./alchemy_tutorial/sql_raw_database_01.db', echo=True)
# echo=True es el verbose para ver que sucede paso a paso

connection = engine.connect()

# This is a SQL CREATE example:
#connection.execute(text("CREATE TABLE IF NOT EXISTS people (name str, age int)"))
connection.execute(text("CREATE TABLE IF NOT EXISTS people2 (name TEXT, age INTEGER)"))

connection.commit()

mysession = Session(engine)

mysession.execute(text('INSERT INTO people2 (name, age) VALUES ("Mike", 30);'))
mysession.commit()