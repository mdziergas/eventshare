import pymongo
import datetime
import os
import bcrypt

mongo = os.environ.get("MONGO")

client = pymongo.MongoClient(mongo)

db = client['eventshare']

users = db['users']
groups = db['groups']

# hashing models
def is_valid_signup(email, username, password, password2):
    if len(email) < 4:
        data={
             'message':'Email must be greater than 4 chars',
             'category':'error'
         }
        return data
    elif len(username) < 2:
        data={
             'message':'Username must be greater than 2 chars',
             'category':'error'
         }
        return data
    elif password != password2:
        data={
             'message':'Passwords must match',
             'category':'error'
         }
        return data
           
    elif len(password) < 8:
        data={
             'message':'Passwords must match',
             'category':'error'
         }
        return data
    else:
        data={
             'message':'Account created.',
             'category':'success'
         }
        return data

def is_valid_login(username, password):
    user = db.users.find_one({'username':username})
    if user:
        hashed_pw = user['password']
        do_pw_match = compare_password(password, hashed_pw)
        if do_pw_match == True:
            return True
        else:
            return False
    return False
        
            
# hashes and returns password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf8'), salt)
    return hashed_pw.decode('utf8')
#compares non hashed and hashed passwords
def compare_password(password, hashed_pw):
    if bcrypt.checkpw(password.encode('utf8'), hashed_pw.encode('utf8')):
        print("match")
        return True
    else:
        return False

# database models 
def add_user(username, email, password):
    hash_pw = hash_password(password)
    user_data = {
        'username': username,
        'email': email,
        'password': hash_pw,
        'groups':[],
    }
    return users.insert_one(user_data)

def add_group(group_id, username, group_name, group_description):
    group_data = {
        '_id': group_id,
        'group_name': group_name,
        'group_description': group_description,
        'username': username,
        'members':[username,],
    }
    return groups.insert_one(group_data)

def add_member_to_group(username, group_id, group_name):
    member_data = {
        'username': username,
    }
    query = {"_id":group_id}
    data = {"$push":{'members': username}}

    query_user = {"username": username}
    data_user = {"$push":{'groups': {'_id':group_id, 'group_name':group_name}}}
    users.update_one(query_user, data_user)
    return groups.update_one(query, data)
