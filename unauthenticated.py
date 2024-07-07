import requests
import sqlite3
import datetime
from dotenv import load_dotenv
import os 
from general import resource_path


basedir = os.path.dirname(__file__)
db_path = os.path.join(basedir, 'db.db')

load_dotenv()

base_url = os.environ['BASE_URL']

def login(username, password):
    try:
        response = requests.post(f'{base_url}authentication/apis/jwt/login/', {
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            return save_auth_credentials(username, response.json())

        else:
            return "something went wrong"
    
    except requests.exceptions.ConnectionError:
        return "server is currently down"
 
def save_auth_credentials(username, creds):
    con = sqlite3.connect(resource_path('db.db'))
    cursor = con.cursor()

    res = cursor.execute("""
    SELECT name FROM sqlite_master WHERE type='table' AND name='user'
    """)

    if len(res.fetchall()) == 0:
         cursor.execute("CREATE TABLE user(username TEXT NOT NULL UNIQUE,access_token TEXT NOT NULL, refresh_token TEXT NOT NULL)")

    
    user = cursor.execute(f"SELECT username FROM user WHERE username = '{username}'")
    if len(user.fetchall()) == 1:
        cursor.execute(f"""
        UPDATE user SET access_token='{creds['access']}', refresh_token='{creds['refresh']}' WHERE username = '{username}'
        """)
    else:
        cursor.execute(f"""
        INSERT INTO user VALUES('{username}', '{creds['access']}', '{creds['refresh']}')
        """)

    con.commit()
    con.close()


    return True


def table_exists(table_name, cursor):

    res = cursor.execute(f"""
    SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'
    """)
    all_ = res.fetchall()
    if len(all_) == 0:
        return False
    elif len(all_) == 1:
        return True
    else:
        return -1


def create_tables(only=True, cursor=None):
    if cursor is None:
        con = sqlite3.connect(resource_path('db.db'))
        cursor = con.cursor()

    list_res = cursor.execute("""
    SELECT name FROM sqlite_master WHERE type='table' AND name='list'
    """)
    
    list_all = list_res.fetchall()
    
    if len(list_all) == 0:
        cursor.execute("""
        CREATE TABLE 
        list(
        list_id INTEGER PRIMARY KEY NOT NULL,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        done INTEGER DEFAULT 0
        )
        """)


    mission_res = cursor.execute("""
    SELECT name FROM sqlite_master WHERE type='table' AND name='mission'
    """)
    mission_all = mission_res.fetchall()

    if len(mission_all) == 0:
        cursor.execute("""
        CREATE TABLE 
        mission(
        mission_id INTEGER PRIMARY KEY NOT NULL,
        list_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        done INTEGER DEFAULT 0
        )
        """)
    
    if only:
        con.commit()
        con.close()
    
    return


def create_list(list_data, missions_data):
    con = sqlite3.connect(resource_path('db.db'))
    cursor = con.cursor()

    list_exists = table_exists('list', cursor)
    missions_exists = table_exists('mission', cursor)

    if not list_exists or not missions_exists:
        create_tables(only=False, cursor=cursor)
    

    try:
        cursor.execute(f"""
        INSERT INTO list (title, date) VALUES('{list_data['title']}', '{list_data['date']}')
        """)
        
        list_id = cursor.lastrowid
        for mission in missions_data:
            cursor.execute(f"INSERT INTO mission (list_id, content) VALUES({list_id}, '{mission['content']}')")

        con.commit()
        con.close()
        return 1
    except:
        return 0


def update_mission(mission_id, col, val):
    con = sqlite3.connect(resource_path('db.db'))
    cursor = con.cursor()

    if type(val) == str:
        val = f"'{val}'"

    cursor.execute(f"""
    UPDATE mission SET {col} = {val} WHERE mission_id = {mission_id}
    """)

    con.commit()
    con.close()

    return 1

def update_list(list_id, col, val):
    con = sqlite3.connect(resource_path('db.db'))
    cursor = con.cursor()

    if type(val) == str:
        val = f"'{val}'"

    cursor.execute(f"""
    UPDATE list SET {col} = {val} WHERE list_id={list_id}
    """)

    con.commit()
    con.close()

    return

def delete_list(list_id):
    con = sqlite3.connect(resource_path('db.db'))
    cursor = con.cursor()

    cursor.execute(f"""
    DELETE FROM mission WHERE list_id = {list_id}
    """)

    cursor.execute(f"""
    DELETE FROM list WHERE list_id = {list_id}
    """)

    con.commit()
    con.close()

    return


def get_today_list():
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')

    con = sqlite3.connect(resource_path('db.db'))
    cursor = con.cursor()

    list_exists = table_exists('list', cursor)
    mission_exists = table_exists('mission', cursor)

    if not list_exists or not mission_exists:
        create_tables(only=False, cursor=cursor)

        return {'title': '', 'tasks': []}

    res_1 = cursor.execute(f"""
            SELECT * FROM list WHERE date = '{str(today_date)}'
          """)
    list_data = res_1.fetchone()
    if list_data is not None:
        res_2 = cursor.execute(f"""
            SELECT * FROM mission WHERE list_id = {list_data[0]}
            """)
        missions_data = res_2.fetchall()


        data = {
            'id': list_data[0],
            'title': list_data[1],
            'tasks': [{'content': mission[2], 'done': mission[3], 'id': mission[0]} for mission in missions_data]
        }

        return data

    return {'title': '', 'tasks': []}
    



def get_list(list_id):
    con = sqlite3.connect(resource_path('db.db'))
    cursor = con.cursor()

    res = cursor.execute(f"SELECT * FROM list WHERE list_id = {list_id}")
    list_tuple = res.fetchone()

    res_2 = cursor.execute(f"SELECT * FROM mission WHERE list_id = {list_id}")
    mission_tuples_list = res_2.fetchall()

    data = {
        "id": list_tuple[0],
        "title": list_tuple[1],
        "date": list_tuple[2],
        "done": list_tuple[3],
        
        "missions": [

        ]
    }

    for mission in mission_tuples_list:
        mission_data = {
            "id": mission[0],
            "list_id": mission[1],
            "content": mission[2],
            "done": (mission[3] == 1)
        }
        data['missions'].append(mission_data)
    
    con.close()

    return data


def get_lists():
    con = sqlite3.connect(resource_path('db.db'))
    cursor = con.cursor()

    res = cursor.execute("SELECT * FROM list ORDER BY list_id DESC")
    lists = res.fetchall()
    keys = {
        'list_id': 0,
        'title': 1,
        'date': 2,
        'done': 3
    }

    con.close()

    return lists, keys


