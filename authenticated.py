import requests
import sqlite3
import datetime
from dotenv import load_dotenv
import os
from general import resource_path

basedir = os.path.dirname(__file__)
db_path = os.path.join(basedir, 'db.db')

load_dotenv(dotenv_path=os.path.join(basedir, '.env'))

access_token = None
refresh_token = None
base_url = os.environ['BASE_URL'] 
global_headers = None

def set_creds():
    global access_token
    global refresh_token
    global global_headers


    try:
        con = sqlite3.connect(resource_path('db.db'))
        cursor = con.cursor()

        res = cursor.execute(f"""
        SELECT * FROM user
        """)

        data_tuple = res.fetchone()
       
        if data_tuple is None:
            return False
            
        creds = {'access_token': data_tuple[1], 'refresh_token': data_tuple[2]}

        global_headers = {
            'Authorization': 'Bearer ' + creds['access_token']
        }


        access_token = True
        refresh_token = creds['refresh_token']

        con.commit()
        con.close()

        return True
    
    except sqlite3.OperationalError:
        return False

def get_request_response(response):

    if response.status_code == 200:
        data = response.json()

        return data
        
    elif response.status_code == 404:
        return 404

    else:
        return -1

def create_list(list_data, missions_data):
    if access_token is not None:
        
        global global_headers
        data = {
            'list': list_data,
            'missions': missions_data
        }

        response = requests.post(f'{base_url}missions/apis/lists/',json=data, headers=global_headers)

        if response.status_code == 201:
            return 1
        
        elif response.status_code == 400:
            return 0
        
        else: # In case status code where 500 or any other problem
            return -1

def get_list(list_id):
    if access_token is not None:
        global global_headers
        response = requests.get(f'{base_url}missions/apis/lists/{list_id}/', headers=global_headers)
        
        return get_request_response(response)


def get_lists():
    if access_token is not None:
        global global_headers

        response = requests.get(f'{base_url}missions/apis/lists/', headers=global_headers)

        keys = {
            'list_id': 'id',
            'title': 'title',
            'date':'date',
            'done': 'done'
        }

        return get_request_response(response), keys


def get_today_list():

    if access_token is not None:
        global global_headers
        try:
            today_date = datetime.datetime.today().strftime('%Y-%m-%d')
            
            response = requests.get(f'{base_url}missions/apis/lists/today/{today_date}/', headers=global_headers)
            
            if response.status_code == 200:
                return response.json()
            if response.status_code == 404:
                return {'title': '', 'missions': []}
            if response.status_code == 403 or response.status_code == 401:
                logout()
                return -1

        except requests.exceptions.ConnectionError:
            return -1
        # return get_request_response(response)

def update_mission(mission_id, data):
    if access_token is not None:
        global global_headers
        response = requests.patch(f'{base_url}missions/apis/missions/{mission_id}/', data=data, headers=global_headers)

        if response.status_code == 202 or response.status_code == 200:
            return 1
        elif response.status_code == 400:
            return 0
        else:
            return -1 

def delete_list(list_id):
    if access_token is not None:
        global global_headers
        response = requests.delete(f'{base_url}missions/apis/list/{list_id}/', headers=global_headers)

        if response.status_code == 204:
            return 1
        else:
            return -1
        
def logout():
    global access_token
    global refresh_token
    global global_headers

    try:
        con = sqlite3.connect(resource_path('db.db'))
        cursor = con.cursor()

        res = cursor.execute(f"""
        SELECT * FROM user
        """)

        data_tuple = res.fetchone()

        cursor.execute(f"""
        DELETE FROM user WHERE username="{data_tuple[0]}"
        """)

        con.commit()
        con.close()

        access_token = None
        refresh_token = None
        global_headers = None

        return

    except sqlite3.OperationalError:
        return False