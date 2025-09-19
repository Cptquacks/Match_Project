import json
STD_UserForm : dict = {
    "Baned" : True,
    "Photo" : None,
    "Name" : None,
    "Age" : None,
    "Info" : None,
    "Gender" : None,
    "Preference" : None
}

#CRUD System
def create_user(user_ID : int, user_Data : dict) -> None:
    if check_user(user_ID) :
        return
    
    new_DB : dict = get_DB()
    new_DB[user_ID] = user_Data

    update_DB(new_DB)

def read_user(user_ID : int) -> dict: #Returns entire userform
    if not check_user(user_ID) :
        return {}
    
    try:
        return get_DB()[f'{user_ID}']
    
    except KeyError:
        pass

    return {}

def update_user(user_ID : int, new_Data : dict) -> None:
    if not check_user(user_ID) :
        return

    user_Data : dict = read_user(user_ID)
    
    if user_Data == new_Data:
        return
    
    for key, value in user_Data.items():
        if (new_Data[key] != value) :
            user_Data[key] = new_Data[key]

    new_DB : dict = get_DB()
    new_DB[user_ID] = user_Data

    update_DB(new_DB)

def delete_user(user_ID : int) -> None:
    if not check_user(user_ID) :
        return
    
    new_DB : dict = get_DB()
    new_DB.pop(f'{user_ID}')

    update_DB(new_DB)

#DB methods
def get_DB() -> dict:
    with open(file = 'Data/user_DB.json', mode = 'r', encoding = 'UTF-8') as JSON_Load:
        return json.load(JSON_Load)
    
    return {}

def update_DB(new_Data : dict) -> None:
    if get_DB == new_Data:
        return
    
    with open(file = 'Data/user_DB.json', mode = 'w', encoding = 'UTF-8') as JSON_Load:
        json.dump(new_Data, JSON_Load)

def check_user(user_ID : int) -> bool:
    if get_DB().__contains__(f'{user_ID}') : 
        return True
    
    return False