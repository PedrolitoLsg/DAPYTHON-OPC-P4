from controller import Controller
from tinydb import TinyDB, Query
query = Query()
database = TinyDB('db.json')
Controller().main_menu()
