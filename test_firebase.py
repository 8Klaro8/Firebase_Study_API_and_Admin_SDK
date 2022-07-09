import json
import time

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

start_friend_id = '0'

class MyFireBase():
    def sign_up(self, email, password):
        self.app = App.get_running_app()  # root for the MainApp inside test_main.py

        '''Create user with admin sdk'''
        try:
            # user = auth.create_user(email=email, password=password) # creates user in the auth
            self.user = config_auth.create_user_with_email_and_password(email, password)
            user_uid = self.user['localId']

            config_db.child('users').update({user_uid: {'email': self.user['email'],
                                                        'avatar': 'avatar_pic.png',
                                                        'streak': 0,
                                                        'my_friend_id': '%s' % self.friend_id_handler(),
                                                        'friends': '',
                                                        'workouts': ''}})
            user_local_id = self.user['localId']
            self.friend_list = config_db.child('users').child(user_local_id).child('friends').get().val()
            self.change_screen('home_screen'),
            print('User logged in')

        except BaseException as e:
            try:
                if json.loads(e.args[1])['error']['message'] == 'INVALID_EMAIL':
                    self.app.root.ids['login_screen'].ids['login_message'].text = 'Invalid email format'
                print(e)
                try:
                    err_message = json.loads(e.args[1])['error']['message']
                    if err_message == 'EMAIL_EXISTS':
                        self.app.root.ids['login_screen'].ids['login_message'].text = 'This user already exists!'
                except:
                    config_db.child('users').child('example_user').set({'fake_key':'fake_value'})
                    print('except')
            except:
                with open('friend_id_storage.txt', 'w') as f:
                    f.write(start_friend_id)

    ''''Creates file to store friend id and reads it'''
    def friend_id_handler(self):
        try:
            with open('friend_id_storage.txt', 'r') as f:
                current_friend_id = f.read()
                next_friend_id = int(current_friend_id) + 1
                next_friend_id = str(next_friend_id)

                with open('friend_id_storage.txt', 'w') as f:
                    f.write(next_friend_id)
        except:
            with open('friend_id_storage.txt', 'w') as f:
                next_friend_id = f.write(start_friend_id)
            print('NOPE')
        return next_friend_id

    def sign_in(self, email, password):
        # TODO hndle missing password exception
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
        config_auth.current_user = None
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

        # current_user = config_auth.current_user

        config_db.child('users').child(self.user['localId']).update({'avatar': image})

        self.app.root.ids['screen_manager'].transition.direction = 'right'
        self.change_screen("settings_screen")

    def get_current_screen(self):
        screen_manager = self.app.root.ids['screen_manager']
        current_screen = screen_manager.current
        # TODO - display log out button only if the user is logged in

        return current_screen

    def add_friend(self, friend_id):
        pass
        try:
            friend_exists = config_db.child('users').order_by_child('my_friend_id').equal_to(str(friend_id)).get()
            if friend_exists[0].val()['my_friend_id'] == friend_id:
                # TODO program crashes when I try to log out and then add friend
                if self.user != None:
                    # TODO Correct error: TypeError: 'NoneType' object is not subscriptable

                    user_local_id = self.user['localId']
                    friends_value = config_db.child('users').child(user_local_id).child('friends').get().val()
                    if friend_id == config_db.child('users').child(user_local_id).child('my_friend_id').get().val():
                        self.app.root.ids['add_friend_screen'].ids[
                            'friend_id_message'].text = f'You cant add yourself as friend'
                    elif friend_id in friends_value:
                        self.app.root.ids['add_friend_screen'].ids[
                            'friend_id_message'].text = f'{friend_id} is already your friend'

                    else:
                        new_friends_value = f'{friends_value}, {friend_id}'
                        config_db.child('users').child(user_local_id).update({"friends": "%s" % new_friends_value})
                        self.app.root.ids['add_friend_screen'].ids[
                            'friend_id_message'].text = f'{friend_id} added to your friend list'


        except IndexError:
            self.app.root.ids['add_friend_screen'].ids['friend_id_message'].text = f'There is no user with this Id: {friend_id}'


