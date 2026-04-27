## SQL Lite DB Creation

1. main.py:
	import sqlite3

2. Create a connection to a new DB
	db = sqlite3.connect("books-collection.db") 

3.  Run main.py to create db file -> VENV dir

4. Next we need to create a cursor which will control our database.
	cursor = db.cursor()

5. Create Tables
	cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")

6. SQL Viewer:
https://sqlitebrowser.org/dl/
	Mac terminal:
	sqlite3 nombre_de_tu_archivo.db para abrir la consola de SQLite.

## Framworks de DB
	Pequeños
		SQL Alchemy
		SQL Model
		Pewee
	
		Django ORM
		Tortoise ORM (Async / await)
		Postgre Psycopg

Resumen de alternativas por categoría
Categoría 	Módulo Destacado	Características

ORM Asíncrono	Tortoise ORM	Inspirado en Django, diseñado específicamente para trabajar con async/await (muy usado con FastAPI).

Bajo nivel (Drivers)	PyMySQL / mysqlclient	Los conectores estándar para bases de datos MySQL.

Drivers (SQL Server)	pyodbc	El estándar para conectar Python con bases de datos de Microsoft.

Query Builders	Pypika	Te permite construir consultas SQL de forma programática sin ser un ORM completo.

---


## Documentation
# SQL
https://www.codecademy.com/article/sql-commands
https://www.w3schools.com/sql/sql_ref_create_table.asp

# SQL Alchemy
https://docs.sqlalchemy.org/en/20/tutorial/index.html
YouTube:
https://www.youtube.com/watch?v=529LYDgRTgQ


# Flask - SQLAlchemy
https://flask-sqlalchemy.palletsprojects.com/en/stable/quickstart/


---
## VENV instructions
Crea el entorno virtual:
	python3 -m venv  <.venv> -> <.venv> es es el folder name

Activa el entorno e instala lo que necesites:
	source .venv/bin/activate
pip install requests (por ejemplo)

echo “.venv/" > .gitignore


To Clean install packages in a .venv
python3 -m pip install my_package

To Clean uninstall packages:
pip uninstall -r requirements.txt -y

To save requirements to .txt
pip freeze > requirements.txt
