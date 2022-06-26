import json

import firebase_admin
from firebase_admin import credentials, db, auth, exceptions
from dotenv import load_dotenv
import os
import requests

load_dotenv()

'''PROJECT URL'''
url = 'https://test-project-80109-default-rtdb.firebaseio.com/.json'

'''POST'''
to_post = '{"name": "Szalon Falon", "DoB": "2232332323"}'
to_post_2 = '{"name": "Faki Laki", "DoB": "2232332323"}'
to_post_3 = '{"name": "Digi bigi", "DoB": "2232332323"}'
# result = requests.post(url=url, data=to_post_3)

'''DELETE'''
# to_del = 'https://test-project-80109-default-rtdb.firebaseio.com/nickname.json'
# to_del = requests.delete(url=to_del, data=to_del)

'''UPDATE'''
# person_to_update = '-N5UvrOs-6SRHjJm3d8n'
# to_update = '{"nickname": "SzalFal"}'
# update_url = f'https://test-project-80109-default-rtdb.firebaseio.com/{person_to_update}.json'
# result = requests.patch(url=update_url, data=to_update)
# print(result.text)

'''Path to use for delete if necessary'''
dela = "https://test-project-80109-default-rtdb.firebaseio.com/%7B'-N5VdB8mSm-BiL9tZbpf'%7D.json"


'''Test users to update in database'''
second_user_uid = '-N5VmZedi-e8yio3wJUx'
third_user_uid = '-N5VnOtUYnhrDERKoeIn'

'''Update multiple elements with one APi call'''
requests.patch(url=url, data='{"%s/phone_number": "+493434334",'
                            ' "%s/phone_number": "+493434343434"}' % (third_user_uid, second_user_uid))

'''Getting Etag'''
# etag_req = requests.get(url="https://test-project-80109-default-rtdb.firebaseio.com/-N5VmZedi-e8yio3wJUx?X-Firebase-ETag: true")
# print(etag_req.content.decode())

# requests.delete('https://test-project-80109-default-rtdb.firebaseio.com/-N5VnRe0pYS47SIcAa4t.json')








'''Rule to use later:'''
# {
#   "rules": {
#     "public_resource": {
#       ".read": true,
#       ".write": true
#     },
#     "some_resource": {
#       ".read": "auth.uid === 'my-service-worker'",
#       ".write": false
#     },
#     "another_resource": {
#       ".read": "auth.uid === 'my-service-worker'",
#       ".write": "auth.uid === 'my-service-worker'"
#     }
#   }
# }
