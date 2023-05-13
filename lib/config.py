import time, json, os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path) 
from datetime import datetime
from database.db import DB




def is_member_exists(name):
    database = DB("members")
    if database.GetOneData({"name": name}):
        return True
    return False

def save_member(member):
    database = DB("members")
    if not database.GetOneData(member):
        database.AddOneData(member) 

def save_member_options(options):
    database = DB("member-options")
    if not database.GetOneData(options):
        database.AddOneData(options)

def give_member_options(name: int, option: str):
    database = DB("member-options")
    data = database.GetOneData({"name": name})
    if data: 
        return data[option]
    
def update_member_options(name: int, option: str, value: str):
    database = DB("member-options")
    data = database.GetOneData({"name": name})
    data[option] = value
    database.UpdateOne({"name": name}, data)

def save_time(name): 
    database = DB("members")
    database.UpdateOne({"name": name}, {"voice-timer": time.time()})

def calculate_time(name): 
    database = DB("members")
    data = database.GetOneData({"name": name})
    if data['voice-timer'] != 0:
        cal = (time.time() - int(data['voice-timer'])) / 30
        balance = 0
        if data['boost']:
            balance = cal * 15
        else:
            balance = cal * 7
        new_balance = int(data['xp']) + balance
        database.UpdateOne({"name": name}, {"xp": new_balance})


def still_on_voice_channel(name):
    database = DB("members")
    data = database.GetOneData({"name": name})
    newBalance = int(data['xp']) + 50
    database.UpdateOne({"name": name}, {"xp": newBalance})


def get_user_wallet(name):
    database = DB("members")
    data = database.GetOneData({"name": name})
    return data['wallet']


def give_current_time(Hour = True, mint = False, sec = False):
    if Hour:
        Hour = "%H"
    else:
        Hour = ""
    if mint:
        mint = "%M"
    else: 
        mint = ""
    if sec: 
        sec = "%S"
    else: 
        sec = ""
    new = datetime.now()

    making_current_time = new.strftime(Hour+":"+mint+":"+sec)
    return making_current_time

def give_default_roles():
    database = DB("config")
    data = database.GetOneData()
    return data["Server"]['default-roles']

def save_chat_points(name, amount : int):
    database = DB('members')
    data = database.GetOneData({"name": name})
    newBalance = int(data['xp']) + amount * 2
    database.UpdateOne({"name": name}, {"xp": newBalance})

def add_colour_roles(color):
    database = DB('colours')
    if not database.GetOneData(color):
        database.AddOneData(color)

def remove_default_role(role):
    database = DB("config")
    data = database.GetOneData({})
    counter = 0
    for rolename in data['Server']['default-roles']:
        if int(rolename) == int(role):
            del data['Server']['default-roles'][counter]  
        else:
            counter += 1
    database.UpdateOne({}, data)    

def add_default_role(role: int): 
    database = DB("config")
    data = database.GetOneData()
    data['Server']['default-roles'].append(role)
    database.UpdateOne({}, data)
    
def is_default_role_exists(role: int):
    database = DB("config")
    data = database.GetOneData()
    for rolename in data['Server']['default-roles']:
        if int(rolename) == role:
            return True
    return False

def is_default_role_banned(role: int):
    database = DB("config")
    data = database.GetOneData()
    for rolename in data['Server']['not-default']:
        if int(rolename) == role:
            return True
    return False
            
def calculate_points(name, points):
    pass

def make_private_user(name, channel_ID):
    database = DB("private-voice")
    payload = {"name": int(name), "channel_ID": [int(channel_ID)], "channel_count": 1}
    database.AddOneData(payload)

def change_private_user_count(name):
    database = DB("private-voice")
    data = database.GetOneData({"name": name})
    data["channel_count"] += 1
    database.UpdateOne({"name": name}, data)
    
    return data['channel_count']

def change_private_user_channels(name, channel):
    database = DB("private-voice")
    data = database.GetOneData({"name": name})
    data['channel_ID'].append(channel)
    database.UpdateOne({"name": name}, data)

def is_private_user_exists(name):
    database = DB("private-voice")
    if database.GetOneData({"name": name}):
        return True
    return False

def give_private_info(name):
    database = DB("private-voice")
    return database.GetOneData({"name": name})

def del_private_info(name, channel: int):
    counter = 0
    database = DB("private-voice")
    data = database.GetOneData({"name": name})
    for findchannel in data['channel_ID']:
        if int(findchannel) == channel:
            del data['channel_ID'][counter]
        else:
            counter += 1
    database.UpdateOne({"name": name}, data)


def is_private_channel_exist(channel: int):
    database = DB("private-voice")
    data = database.GetAllData()
    for main in data:
        if channel in main['channel_ID']:
            return True
    return False
            
        
def get_user_profile_url(name):
    database = DB("members")
    data = database.GetOneData({"name": name})
    if data is not None:
        return data['avatar']

def get_user_level(name):
    database = DB("members")
    data = database.GetOneData({"name": name})
    if data is not None:
        return data['level']

def get_user_xp(name: int):
    database = DB("members")
    data = database.GetOneData({"name": name})
    if data is not None:
        return data['xp']

def get_colour_roles():
    database = DB("colours")
    data = database.GetAllData()
    if data:
        return data
    
def update_boost_status(name: int, status: bool):
    database = DB("members")
    data = database.GetAllData({"name": name})
    for user in data:
        if user["name"] == name:
            user['boost'] = status
    database.UpdateOne({"name": name}, data)


# Tickets -----------------------------------
def get_current_ticket_id():
    database = DB("tickets")
    data = list(database.GetAllData())
    return len(data) + 1

def update_ticket(ticket: int, payload: dict):
    database = DB("tickets")
    keys, values = zip(*payload.items())
    data = database.GetOneData({'id': ticket})
    counter = 0
    for i in keys:
        data[i] = values[counter]
        counter += 1


    database.UpdateOne({"id": ticket}, data)   

def save_ticket(peyload):
    database = DB("tickets")
    database.AddOneData(peyload)

def get_ticket(id: int):
    database = DB("tickets")
    data = database.GetOneData({'id': id})
    if data: return data

def is_ticket_exists(member: int):
    database = DB("tickets")
    data = database.GetAllData({"user-id": member})
    if data:
        for one in data:
            if not one['deleted']:
                return True
    # return False

        
    

#Admins -------------------------------
def get_list_of_admins():
    database = DB("staff")
    data = database.GetOneData()
    admin_names = []
    for admin in data['admin']:
        admin_names.append(admin['admin-id'])
    return admin_names
def save_admin(payload):
    database = DB("staff")
    data = database.GetOneData()
    data['admin'].append(payload)
    database.UpdateOne({}, data)









# def check_xp_for_lvl(name, defaultPoints):
#     with open("database/member-info.json", 'r') as file:
#         file_to_read = json.load(file)
#         for member in file_to_read:
#             if member['name'] == int(name):
#                 current_xp = member['xp']
#                 if int(current_xp) > int(defaultPoints):

#                     if int(member['level']) == 0:
#                         member['xp'] = int(current_xp) - int(defaultPoints)
#                         member['level'] = int(member['level']) + 1
#                     else:
#                         must_add = 100 * int(member['level'])
#                         must_min = must_add + int(defaultPoints)
#                         member['xp'] = int(current_xp) - must_min
#                         member['level'] = int(member['level']) + 1

# # def calculate_voice_xp(name):
# #     with open("database/member-info.json", 'r') as file:
# #         file_to_read = json.load(file)
# #         for member in file_to_read:
# #             if member['name'] == int(name):
# #                 curre

# # def get_current_status():
# #     with open("database/member-info.json", "r") as file:
# #         file_to_read = json.load(file)
        