import base64
import hashlib

import firebase_admin
import requests
import json
from kivy.app import App
import os
from dotenv import load_dotenv
import pyrebase
from firebase_admin import auth, db, credentials

load_dotenv() # Load env. variables

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
salt_random_number = int(os.getenv('salt_random_number'))
iterations_of_SHA = int(os.getenv('iterations_of_SHA'))
print(type(iterations_of_SHA))
dklen = os.getenv('dklen')
sha_type = os.getenv('sha_type')

'''Pyrebase'''
# my_firebase = pyrebase.initialize_app(firebase_config) # initialize firebase
# config_db = my_firebase.database() # setting up database
# config_auth = my_firebase.auth() # setting up auth

'''Initialize Admin SDK'''
cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
firebase_admin.initialize_app(cred, {'databaseURL': 'https://test-project-80109-default-rtdb.firebaseio.com/'})

'''Play with creating user and error handling'''
# try:
#     config_auth.create_user_with_email_and_password(email, password)
# except requests.exceptions.HTTPError as e:
#     error_message = json.loads(e.args[1])['error']['message']
#     if error_message == 'EMAIL_EXISTS':
#         print('Email exists')

'''Sign in user and set 2 (randomly chosen) attribute to it'''
# try:
#     user = config_auth.sign_in_with_email_and_password(email, password)
#     config_db.child(user['localId']).child("Username").set(name)
#     config_db.child(user['localId']).child("ID").set(user['localId'])
#     print('user signed in')
#     anakin_user = config_db.child('Jhq2ESSnGfcYtSPaeKXloEM5gQB3')
#     anakin_user.child('Username').set(name)
#     anakin_id_token = config_db.child('Jhq2ESSnGfcYtSPaeKXloEM5gQB3').child('Username').get().val()
#     print(f'id_token of anakin: {anakin_id_token}')
#
# except requests.exceptions.HTTPError as er:
#     err_message = json.loads(er.args[1])['error']
#     if err_message == 'Permission denied':
#         print('Permission denied')

# config_db.child('/').update({'kar': {'address': 'mikaja', 'age': '84'}})


'''Help reference to manage data'''
# for data in all_data: # This is how t iterate thru all keys and set value to None
#     curr_child = config_db.child(data.key()).set('')
    # print(curr_child.get().key())
# config_db.child('love').set('margit') # This is how to set value


# for dat in all_data:
#     data_key = config_db.child(dat.key()).get().key()
#
#     print(data_key)


class MyFireBase():
    def sign_up(self, email, password):
        self.app = App.get_running_app() # root for the MainApp inside test_main.py

        '''Create user with pyrebase'''
        # user_created = config_auth.create_user_with_email_and_password(email, password)
        # user_email = user_created['email']
        # config_db.set({user_created['localId']:
        #                {'email': user_email,
        #                 'avatar': 'avatar_pic.png'}})
        #
        # print(f"local id in test_firebase.py: {user_created['localId']}")


        '''Create user with admin sdk'''
        try:
            user = auth.create_user(email=email, password=password) # creates user in the auth
            users_ref = db.reference('/')

            # TODO understand and decode firebase hash, to decode the coded password
            # self.generate_derived_key(mem_cost=14, rounds=8, salt_separator='Bw==', salt=)

            '''Generating hashed password'''
            hashed_password = self.hash_pass(password)
            print(f'Hashed password: \n{hashed_password}\n')

            '''Setting user uid as reference to the user in the real time db'''
            # users_ref.child('users').update({user.uid: {'email': user.email,
            #                                             'password': hashed_password.decode('latin-1').strip()}})

            users_ref.child('users').update({user.uid: {'email': user.email,
                                                        'password': password}})

            self.change_screen('home_screen'),
            print('User logged in')
        except auth._auth_utils.EmailAlreadyExistsError:
            self.app.root.ids['login_screen'].ids['login_message'].text = 'Email already exists'


    def sign_in(self, email, password):
        global user
        # TODO get hashed password from db and authenticate user. Only then let them login !!!!!!!!!!!!!!!!!!!!!!!
        self.app = App.get_running_app()
        try:
            current_user = auth.get_user_by_email(email)
            curr_us_uid = current_user.uid

            '''Read avatar image file from db and load it'''
            user_ref = db.reference(f'/users')
            try:
                avatar = user_ref.child(curr_us_uid).child('avatar').get()
                avatar_img = self.app.root.ids['avatar_image']
                avatar_img.source = 'avatars/' + avatar
            except:
                print('no avatar image')

            with open('uid_storage.txt', 'w') as f:
                f.write(curr_us_uid)

            '''check password, only then log in'''
            hashed_password = self.hash_pass(password)

            # read stored password
            # user_to_find = user_ref.order_by_child('email').equal_to(email)
            # passworddddd = list(user_to_find.get().items())[0][1]['password']
            # if passworddddd == hashed_password:
            #     print('OOOOOKKKKKKK')

            self.change_screen('home_screen')

        except auth._auth_utils.UserNotFoundError:
            self.app.root.ids['login_screen'].ids['login_message'].text = 'User does not exist. Sign up!'

    def change_screen(self, screen_name):
        screen_manager = self.app.root.ids['screen_manager']
        screen_manager.current = screen_name

    def change_avatar(self, image, widget_id):
        # Change avatar in app
        avatar_img = self.app.root.ids['avatar_image']
        avatar_img.source = 'avatars/' + image

        # change avatar image in db
        users_ref = db.reference('/users')
        # TODO authenticate current user - get current user
        #  try to save an id when logging in and authenticate using that

        try:
            with open('uid_storage.txt', 'r') as f:
                curr_us_uid = f.read()
            signed_in_user = auth.get_user(curr_us_uid)
            print(signed_in_user.uid)
            users_email = signed_in_user.email

            '''Search by child item'''
            # ordered_ref = db.reference('/users').order_by_child('email').equal_to(users_email)

            user_ref = db.reference(f'/users')
            user_ref.child(signed_in_user.uid).update({'avatar': image})
        except:
            print('file does no exists')
        finally:
            self.change_screen("settings_screen")

    def hash_pass(self, password):
        '''My hash function'''
        salt = os.urandom(32) # Remember this
        key = hashlib.pbkdf2_hmac(
            'sha256',  # The hash digest algorithm for HMAC
            password.encode('utf-8'),  # Convert the password to bytes
            salt,  # Provide the salt
            100000,  # It is recommended to use at least 100,000 iterations of SHA-256
            dklen=128  # Get a 128 byte key
        )


        '''Firebase hash function'''
    def generate_derived_key(
            password: str,
            salt: str,
            salt_separator: str,
            rounds: int,
            mem_cost: int
    ) -> bytes:
        """Generates derived key from known parameters"""
        n = 2 ** mem_cost
        p = 1
        user_salt: bytes = base64.b64decode(salt)
        salt_separator: bytes = base64.b64decode(salt_separator)
        password: bytes = bytes(password, 'utf-8')

        derived_key = hashlib.scrypt(
            password=password,
            salt=user_salt + salt_separator,
            n=n,
            r=rounds,
            p=p,
        )

        return derived_key


