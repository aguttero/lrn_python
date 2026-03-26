## SQL Lite DB Creation

main.py:
import sqlite3
# Create a connection to a new DB
db = sqlite3.connect("books-collection.db") 
# Run main.py to create db file -> VENV dir


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
