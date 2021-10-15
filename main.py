from controller import Controller
from tinydb import TinyDB, Query
query = Query()
db = TinyDB('db.json')
Controller().main_menu()
