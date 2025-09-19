import json

#CRUD System
def create_user(user_ID : str) -> None:
    pass

def read_user(user_ID : str) -> dict:
    return {}

def update_user(user_ID : str) -> None:
    pass

def delete_user(user_ID : str) -> None:
    pass

#DB methods
def get_DB() -> dict:
    with open(file = 'Data/user_DB.json', mode = 'r', encoding = 'UTF-8') as JSON_Load:
        return json.load(JSON_Load)
    
    return {}

def check_user(user_ID : str) -> bool:
    
    return False