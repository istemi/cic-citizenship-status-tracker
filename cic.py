#!/usr/bin/env python3
import boto3
import requests
import datetime
import os


app_client_id = '3hul7n7bbsam21q4vis8vnbf5j'
username = os.environ.get('UCI')
password = os.environ.get('CTZ_PASS')

def citizenship_tracker(username: str, password: str, 
                               app_client_id: str) -> None:
    client = boto3.client('cognito-idp')

    resp = client.initiate_auth(
        ClientId=app_client_id,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password
        }
    )

    print("Log in successfully - Getting data")
    # print("ID token:", resp['AuthenticationResult']['IdToken'])

    headers = {
        "authorization": "Bearer " + resp['AuthenticationResult']['IdToken'],   
    }

    raw_data = '{"method":"get-profile"}'

    response = requests.post('https://api.cst-ssc.apps.cic.gc.ca/user', data=raw_data, headers=headers)
    jsonResponse = response.json()
    print(f"UCI: {username}")
    print(f"STATUS: {jsonResponse['profile']['status']}")
    print(f"LAST UPDATE: {datetime.datetime.fromtimestamp(jsonResponse['profile']['lastUpdatedTime']/1000)}")
    print(f"WAITING: {datetime.datetime.now()-datetime.datetime.fromtimestamp(jsonResponse['profile']['lastUpdatedTime']/1000)}")
    for activity in jsonResponse['profile']['activities']:
        print(f"{activity['activity']} - {activity['status']}")

citizenship_tracker(username, password, app_client_id)
