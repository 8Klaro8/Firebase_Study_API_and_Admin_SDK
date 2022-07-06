import firebase_admin
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from workout_banner import WorkoutBanner
from kivy.uix.label import Label
import requests
import json
import os
from os import walk
from functools import partial
from test_firebase import MyFireBase
from firebase_admin import auth, credentials, db
import pyrebase
import firebase
# import os
# from dotenv import load_dotenv
# load_dotenv()

class HomeScreen(Screen):
    pass
class LabelButton(ButtonBehavior, Label):
    pass
class ImageButton(ButtonBehavior, Image):
    pass
class ChangeAvatarScreen(Screen):
    pass
class LoginScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass


# user = auth.create_user(email='rrr@gmail.com',password='121212')
# users_ref.child('users').push(user.email)



'''Delete all user from DB'''
# users_ref = db.reference('/users')
# users_ref.set('')
# quit()
'''Delete all user from auth'''
# firebase_admin.initialize_app()
# all_user = auth.list_users().users
# all_user_uid = []
# for user in all_user:
#     all_user_uid.append(user.uid)
# for uid in all_user_uid:
#     auth.delete_user(uid)
# quit()


GUI = Builder.load_file('main.kv')

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
# cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
# firebase_admin.initialize_app(cred)

'''Setting up pyrebase'''
firebase_config = {
    'apiKey': "AIzaSyCmDTaaINrZtn6HmA-Kb9hTgnBCaZmEABM",
    'authDomain': "friendly-fitness-9b323.firebaseapp.com",
    'databaseURL': "https://friendly-fitness-9b323-default-rtdb.firebaseio.com",
    'projectId': "friendly-fitness-9b323",
    'storageBucket': "friendly-fitness-9b323.appspot.com",
    'messagingSenderId': "1418575742",
    'appId': "1:1418575742:web:0bf5c22179566e2049bd2f",
    'measurementId': "G-3ZJKT5F4BQ",
    'serciveAccount': GOOGLE_APPLICATION_CREDENTIALS
}
my_firebase = pyrebase.initialize_app(firebase_config)
config_auth = my_firebase.auth()
config_db = my_firebase.database()


'''Start running main app'''
class MainApp(App):
    def build(self):
        self.my_firebase = MyFireBase()
        return GUI

    def on_start(self):
        # Populate avatar grid
        avatar_grid = self.root.ids['change_avatar_screen'].ids['avatar_grid']
        for root_dir, folder, file in walk("avatars"):
            for f in file:
                img = ImageButton(source="avatars/" + f, on_release=partial(self.my_firebase.change_avatar, f))
                avatar_grid.add_widget(img)


            # Get and update streak label
            # streak_label = self.root.ids['home_screen'].ids['streak_label']
            # streak_label.text = str(data['streak']) + ' Day Streak!'

            # Get and update friend ID label
            # friend_id_label = self.root.ids['settings_screen'].ids['friend_id_label']
            # friend_id_label.text = 'Friend ID: ' + str(data['friend_id_label'])
            # Get banner grid
            # banner_grid = self.root.ids['home_screen'].ids['banner_grid']
            # for workout in workouts:
            #     for i in range(5):
            #         # Populate workout grid in home screen
            #         w = WorkoutBanner(workout_image=workout['workout_image'], description=workout['description'],
            #                           type_image=workout['type_image'], number=workout['number'], units=workout['units'],
            #                           likes=workout['likes'])
            #         banner_grid.add_widget(w)

            # self.change_screen('home_screen')

        # except Exception as e:
        #     print(f'Something wrong with: {e}')
        #     pass


    def change_screen(self, screen_name):

        # Gets the screen manager from the root
        screen_manager = self.root.ids['screen_manager']

        # Sets the current screen to the screen that was passed
        # in as parameter in homescreen.kv - app.change_screen
        screen_manager.current = screen_name


MainApp().run()
