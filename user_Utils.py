import json

STD_Set : dict = {
    'name' : '',
    'like' : [],
    'info' : '',
    'gender' : None,
    'prefer' : None
}

#DB functions
def get_DB() -> dict:
    with open(file = 'Data/user_DB.json', mode = 'r', encoding = 'UTF-8') as load:
        return json.load(load)

def set_DB(new_DB : dict) -> None:
    with open(file = 'Data/user_DB.json', mode = 'w', encoding = 'UTF-8') as dump:
        json.dump(new_DB, dump)
#END

def get_user(user : int) -> dict:
    try :
        return get_DB()[f'{user}']
    
    except IndexError:
        return {}
    
def has_user(user : int) -> bool:
    return get_DB().__contains__(f'{user}')
    
def create_user(user : int, data_set : dict) -> None:
    new_DB : dict = get_DB()
    new_DB[user] = data_set

    set_DB(new_DB = new_DB)

def edit_user(user : int, data_set : dict) -> None:
    if not has_user(user) :
        return
    
    new_DB : dict = get_DB()
    user_Data : dict = get_user(user)

    user_Data = data_set
    new_DB[user] = user_Data

    set_DB(new_DB)

