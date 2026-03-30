import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///./alchemy_tutorial/mydatabase2.db', echo=True)
# engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/tutorial_database.db', echo=True)
# Se puede cambiar el motor de la DB. Abstraccion de capas de Alchemy
# echo=True es el verbose para ver que sucede paso a paso

dataframe= pd.read_sql("SELECT * FROM people", con=engine)
print (dataframe)
print ("- - - - * "*3)

new_data = pd.DataFrame({
    "name": ['Florian','Jack'],
    "age": [26,90]
})

new_data.to_sql('people', con=engine, if_exists='append', index=False)

dataframe= pd.read_sql("SELECT * FROM people", con=engine)
print (dataframe)
