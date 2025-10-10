import json
STD_UserForm : dict = {
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
    
    print("- Fetching DB")
    new_DB : dict = get_DB()

    print("- Creating user Data")
    new_DB[user_ID] = user_Data

    print("* Calling update method")
    update_DB(new_DB)

def read_user(user_ID : int) -> dict: #Returns entire userform
    if not check_user(user_ID) :
        print("[!] User did not pass verification")
        return {}
    
    try:
        print("* Returning user in DB")
        return get_DB()[f'{user_ID}']
    
    except KeyError:
        pass

    return {}

def update_user(user_ID : int, new_Data : dict) -> None:
    if not check_user(user_ID) :
        print("[!] User did not pass verification")
        return
    
    print("- Reading user from DB")
    user_Data : dict = read_user(user_ID)
    if user_Data == new_Data:
        print("[!] Same data")
        return
    
    user_Data = new_Data

    print("- Fetching DB")
    new_DB : dict = get_DB()

    print(f"- Updating user ID:{user_ID}")
    new_DB.pop(f'{user_ID}')
    new_DB[f'{user_ID}'] = user_Data

    print("* Updating DB")
    update_DB(new_DB)

def delete_user(user_ID : int) -> None:
    if not check_user(user_ID) :
        print("[!] User did not pass verification")
        return
    
    print(f"- Fetching data && deleting entry {user_ID}")
    new_DB : dict = get_DB()
    new_DB.pop(f'{user_ID}')

    print(f"* Updating DB")
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

def check_ban(user_ID : int) -> bool:
    try :
        if check_user(user_ID) and read_user(user_ID)['Baned']:
            return True
    except KeyError:
        pass

    return False

def check_user(user_ID : int) -> bool:
    if get_DB().__contains__(f'{user_ID}') : 
        return True
    
    return False

