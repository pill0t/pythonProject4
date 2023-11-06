# import pandas as pd
import requests
import json
import time  ## Get the tokens from file to connect to Strava
import os
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
    access_token = strava_tokens['access_token']    # TODO Check if token expired, if not return token from file else get new token and save it
    expires_at = strava_tokens['expires_at'] #-------------------------

    if time.time() >= expires_at:  #------------------------
        data = {
            'client_id': os.environ.get("CLIENT_ID"),  # Insert here your Client ID from strava
            'client_secret': os.environ.get("CLIENT_SECRET"),  # Here your client secret
            'grant_type': 'refresh_token',
            'refresh_token': strava_tokens["refresh_token"]  # Here your refresh token
        }
        response = requests.post(url='https://www.strava.com/oauth/token', data=data)
        if response.status_code == 200:
            response_json = response.json()
            access_token = response_json['access_token']
            expires_at = response_json['expires_at'] #---------------------
            with open('strava_tokens.json', 'w') as outfile:
                json.dump(response_json, outfile)
        else:
            raise Exception("Failed to refresh access token") #-----------

    return access_token


def get_headers():
    return {"Authorization": f"Bearer {get_access_token()}"}


def get_activity():
    url = "https://www.strava.com/api/v3/activities"
    activity_list = []
    headers = get_headers()
    params = {
        "per_page": 200,
        "page": 1
    }
    while True:
        # get page of activities from Strava
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            activity_list.extend(response_json)
            if len(response_json) < 200:
                break
            params['page'] += 1
        else:
            raise Exception(f"Data collection failed on page : {params['page']}")

    return activity_list


if __name__ == "__main__":
    get_activity()
