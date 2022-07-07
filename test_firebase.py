import json

import firebase
import requests
from kivy.app import App
import os
from dotenv import load_dotenv
import pyrebase
from firebase_admin import auth
from workout_banner import WorkoutBanner


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

            my_friend_id = 0
            config_db.child('users').update({user_uid: {'email': user['email'],
                                                        'avatar': 'avatar_pic.png',
                                                        'streak': 0,
                                                        'my_friend_id': '%s' % my_friend_id,
                                                        'friends': '',
                                                        'workouts': ''}})

            self.change_screen('home_screen'),
            print('User logged in')
        except BaseException as e:
            err_message = json.loads(e.args[1])['error']['message']
            if err_message == 'EMAIL_EXISTS':
                self.app.root.ids['login_screen'].ids['login_message'].text = 'This user already exists!'


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

                # Get and update streak label
                streak_label = self.app.root.ids['home_screen'].ids['streak_label']
                streak_from_db = config_db.child('/users').child(current_user['localId']).child('streak').get().val()
                streak_label.text = 'Streak days in a row: ' + str(streak_from_db)

                # Get and update friend ID label
                friend_id_label = self.app.root.ids['settings_screen'].ids['friend_id_label']
                friend_id_from_db = config_db.child('/users').child(current_user['localId']).child('friend_id_label').get().val()
                friend_id_label.text = 'Friend ID: ' + str(friend_id_from_db)

                # Get banner grid
                banner_grid = self.app.root.ids['home_screen'].ids['banner_grid']
                workouts = config_db.child('/users').child(current_user['localId']).child('workouts').get().val()
                # for www in workouts.items():
                #     print(www[1])
                for workout in workouts.items():
                    for i in range(5):
                        # Populate workout grid in home screen
                        w = WorkoutBanner(workout_image=workout[1]['workout_image'], description=workout[1]['description'],
                                          type_image=workout[1]['type_image'], number=workout[1]['number'], units=workout[1]['units'],
                                          likes=workout[1]['likes'])
                        banner_grid.add_widget(w)


            except:
                # adds avatar key if missing
                config_db.child(user_uid).update({'avatar': 'avatar_pic.png'})

        except BaseException as e:
            print(e)
            err_message = json.loads(e.args[1])['error']['message']
            if err_message == 'EMAIL_NOT_FOUND':
                self.app.root.ids['login_screen'].ids['login_message'].text = 'User does not exist. Sign up!'
            elif err_message == 'INVALID_PASSWORD':
                self.app.root.ids['login_screen'].ids['login_message'].text = 'Password is incorrect'
            elif err_message == 'EMAIL_EXISTS':
                self.app.root.ids['login_screen'].ids['login_message'].text = 'This user name already exists'

    def log_out(self):

        current_user = config_auth.current_user
        current_user = None
        self.change_screen('login_screen')
        avatar_img = self.app.root.ids['avatar_image']
        avatar_img.source = "avatars/avatar_pic.png"


    def change_screen(self, screen_name):
        screen_manager = self.app.root.ids['screen_manager']
        screen_manager.current = screen_name



    def change_avatar(self, image, widget_id):
        # Change avatar in app
        avatar_img = self.app.root.ids['avatar_image']
        avatar_img.source = 'avatars/' + image

        current_user = config_auth.current_user

        config_db.child('users').child(current_user['localId']).update({'avatar': image})

        self.app.root.ids['screen_manager'].transition.direction = 'right'
        self.change_screen("settings_screen")

    def get_current_screen(self):
        screen_manager = self.app.root.ids['screen_manager']
        current_screen = screen_manager.current
        # TODO - display log out button only if theu ser is logged in

        return current_screen


