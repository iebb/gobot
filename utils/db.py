import sqlite3

db = sqlite3.connect("database.db")
cur = db.cursor()


def get_db_cur():
    return db, cur
