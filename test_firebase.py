
from kivy.app import App
import os
from dotenv import load_dotenv
import pyrebase
from firebase_admin import auth

load_dotenv() # Load env. variables

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

'''Pyrebase'''
firebaseConfig = {
    'apiKey': "AIzaSyAV8XcBYsI11P15Asy1Vtm7k4uwsSdKDtw",
    'authDomain': "test-project-80109.firebaseapp.com",
    'databaseURL': "https://test-project-80109-default-rtdb.firebaseio.com",
    'projectId': "test-project-80109",
    'storageBucket': "test-project-80109.appspot.com",
    'messagingSenderId': "1009245828697",
    'appId': "1:1009245828697:web:a46bc86feec4e064882348",
    'measurementId': "G-T086LY8ESC",
    'serciveAccount': GOOGLE_APPLICATION_CREDENTIALS
}

my_firebase = pyrebase.initialize_app(firebaseConfig) # initialize firebase
config_db = my_firebase.database() # setting up database
config_auth = my_firebase.auth() # setting up auth

class MyFireBase():
    def sign_up(self, email, password):
        self.app = App.get_running_app() # root for the MainApp inside test_main.py

        '''Create user with admin sdk'''
        try:
            # user = auth.create_user(email=email, password=password) # creates user in the auth
            user = config_auth.create_user_with_email_and_password(email, password)
            user_uid = user['localId']

            config_db.child('users').update({user_uid: {'email': user['email'],
                                                        'avatar': 'avatar_pic.png'}})

            self.change_screen('home_screen'),
            print('User logged in')
        except auth._auth_utils.EmailAlreadyExistsError:
            self.app.root.ids['login_screen'].ids['login_message'].text = 'Email already exists'


    def sign_in(self, email, password):
        self.app = App.get_running_app()
        try:
            config_auth.sign_in_with_email_and_password(email, password)
            current_user = config_auth.current_user
            user_uid = current_user['localId']
            try:
                avatar = config_db.child('users').child(user_uid).child('avatar').get() # Get avatar image in DB
                avatar_img = self.app.root.ids['avatar_image'] # Get avatar image source from kivy
                avatar_img.source = 'avatars/' + avatar.val()
                self.change_screen('home_screen')
            except:
                # adds avatar key if missing
                config_db.child(user_uid).update({'avatar': 'avatar_pic.png'})



        except auth._auth_utils.UserNotFoundError:
            self.app.root.ids['login_screen'].ids['login_message'].text = 'User does not exist. Sign up!'

    def change_screen(self, screen_name):
        screen_manager = self.app.root.ids['screen_manager']
        screen_manager.current = screen_name

    def change_avatar(self, image, widget_id):
        # Change avatar in app
        avatar_img = self.app.root.ids['avatar_image']
        avatar_img.source = 'avatars/' + image

        current_user = config_auth.current_user

        config_db.child('users').child(current_user['localId']).update({'avatar': image})
        self.change_screen("settings_screen")


