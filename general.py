import sqlite3
import os 
import sys

basedir = os.path.dirname(__file__)
db_path = os.path.join(basedir, 'db.db')

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)

def set_theme(theme):
    con = sqlite3.connect(resource_path('db.db'))
    cursor = con.cursor()

    res = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='theme'")

    if res.fetchone() is None:
        cursor.execute("CREATE TABLE theme(id INTEGER PRIMARY KEY NOT NULL, value TEXT)")
    
        
    if cursor.execute("SELECT * FROM theme WHERE id=1").fetchone() is None:
        cursor.execute(f"INSERT INTO theme (value) VALUES('{theme}')")
        
    else:
        cursor.execute(f"UPDATE theme SET value='{theme}' WHERE id=1")

    con.commit()
    con.close()

    return theme


def get_theme():
    con = sqlite3.connect(resource_path('db.db'))
    cursor = con.cursor()


    res = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='theme'")
    
    if res.fetchone() is None:
        cursor.execute("CREATE TABLE theme(id INTEGER PRIMARY KEY NOT NULL, value TEXT)")

        con.commit()
        con.close()
        return 'system'

    res = cursor.execute("SELECT value FROM theme WHERE id=1")
    value = res.fetchone()
    if value is None:
        return 'system'

    return value[0]
