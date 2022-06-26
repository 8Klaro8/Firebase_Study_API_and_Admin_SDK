import json

import firebase_admin
from firebase_admin import credentials, db, auth, exceptions
from dotenv import load_dotenv
import os
import requests

load_dotenv()

'''---------------create user link = FireBase---------------------------:
https://firebase.google.com/docs/auth/admin/manage-users#create_a_user'''






# Getting the web api key
WAK = os.getenv('WAK') # Web Api Key
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# initializing basic firebase app
cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://test-project-80109-default-rtdb.firebaseio.com/',
    'databaseAuthVariableOverride': None
        # {
        #     'uid': 'my-service-worker'
        # }
})

# setting up root
root = db.reference()

# creating users key
# root.update({'users': ''})


EMAIL_INPUT = 'user14@example.com'

try:
    check_user_exists = auth.get_user_by_email(EMAIL_INPUT)
    print(f'User exists: {check_user_exists.email}')
    print(f'With username: {check_user_exists.display_name}')
except:
    print('User not registered')
    add_new_user = input('add new user?')
    if add_new_user == 'y':

        # creating new user
        new_user = auth.create_user(
            email=EMAIL_INPUT,
            email_verified=False,
            phone_number='+15555550114',
            password='secretPassword',
            display_name='John Doe',
            photo_url='http://www.example.com/12345678/photo.png',
            disabled=False)

        # Getting data from new user (to append it to real time database)
        new_user_email = new_user.email
        new_user_phone_number = new_user.phone_number
        new_user_name = new_user.display_name
        new_user_uid = new_user.uid

        # add new user to realtime db
        root.child('users').update({new_user_name:
            {
                'email': new_user_email,
                'phone_number': new_user_phone_number,
                'uid': new_user_uid,

            }})

        # TODO - handle unauthenticated exception


        print('new user added')

quit()

# set up uid
# UID = os.getenv('UID')

# Create user
user_1 = auth.create_user(
    email=EMAIL_INPUT,
    email_verified=False,
    phone_number='+15555550105',
    password='secretPassword',
    display_name='John Doe',
    photo_url='http://www.example.com/12345678/photo.png',
    disabled=False)
print('Sucessfully created new user: {0}'.format(user_1.uid))
gen_user_uid = user_1.uid
# quit()

# creating custom token with uid
custom_token = auth.create_custom_token(gen_user_uid)
user = auth.get_user_by_email('user1@example.com')
curr_user = firebase_admin.auth.get_user(gen_user_uid)
print(f'user: {curr_user.display_name}')
quit()


# endpoint to get id_token, refresh_token
auth_endpoint = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={WAK}'
request_payload = '{"token":"%s","returnSecureToken":true}' % custom_token

request_payload = requests.get(url=auth_endpoint, data=request_payload)

print(request_payload)
quit()

response_payload = requests.get(url=auth_endpoint, data=request_payload)








first_user = requests.get('https://test-project-80109-default-rtdb.firebaseio.com/1.json')
data = json.loads(first_user.content.decode())
print(data['workouts'])

new_workout = '{"abs": "8"}'
requests.patch(url='https://test-project-80109-default-rtdb.firebaseio.com/1.json', data=new_workout)



quit()

'''DOC for learning: https://firebase.google.com/docs/admin/setup/#python'''


# Get the path of the json file - aka: New Private Key
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

# creating credentials with the private key - above
cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)

# initialize the app with the credentials and the api key to my project
default_app = firebase_admin.initialize_app(
    cred,
    {'databaseURL': 'https://test-project-80109-default-rtdb.firebaseio.com/'})

# get reference of my first branch set up
first_user = db.reference('1')
first_user.set({'workouts': {
    'pull-ups': {
        'units': 'sets',
        'volume': 'hard'
    },
    'push_ups': {
        'units': 'sets',
        'volume': 'extra hard'
    }
}})

workouts_update = db.reference('1/')
workouts_update.update(
    {'workout':{
        'sit_ups': {
            'units': 'sets',
            'volume': 'legend'
        }
}})
print(workouts_update.get())
# print(first_user.get())



