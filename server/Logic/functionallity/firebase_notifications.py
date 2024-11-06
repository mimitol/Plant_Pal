"""Server Side FCM sample.

Firebase Cloud Messaging (FCM) can be used to send messages to clients on iOS,
Android and Web.

This sample uses FCM to send two types of messages to clients that are subscribed
to the `news` topic. One type of message is a simple notification message (display message).
The other is a notification message (display notification) with platform specific
customizations. For example, a badge is added to messages that are sent to iOS devices.
"""

import argparse
import json
import requests
import google.auth.transport.requests
from google.oauth2 import service_account

PROJECT_ID = 'plants-fire-base'
BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

# [START retrieve_access_token]
def get_access_token():
  credentials = service_account.Credentials.from_service_account_file(
    '/Configuration/service-account.json', scopes=SCOPES)
  request = google.auth.transport.requests.Request()
  credentials.refresh(request)
  print(credentials.token)
  return credentials.token
# [END retrieve_access_token]

def send_fcm_message(plant_name,token_of_user,user_name):
  # [START use_access_token]
  headers = {
    'Authorization': 'Bearer ' + get_access_token(),
    'Content-Type': 'application/json; UTF-8',
  }
  # [END use_access_token]
  resp = requests.post(FCM_URL, data=json.dumps({'message': {
      'token': token_of_user,
      'notification': {
        'title': f'{user_name}, Dont forget to water your plant!',
        'body': f'plant-pal reminds you- your {plant_name} needs watering'
      }
    }}), headers=headers)



