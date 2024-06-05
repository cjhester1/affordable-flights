import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from pprint import pprint

load_dotenv()

sheety_url = os.getenv("SHEETY_ENDPOINT")

"""
With Basic Auth, a request contains a header field called Authorization, with the value set to the 
username and password encoded as base64. You set the username and password inside of Sheety.

Sheety can generate the Authorization header value for you. Find it inside Authentication settings.
"""


class DataManager:
    #class responsible for communicating w/ Google Sheet.
    def __init__(self):
        #works similar as a token except its a username and password passed into auth field
        self._username = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._username, self._password)  # authorization for our api req
        self.destination_data = {}

    def get_destination_data(self):
        # Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=sheety_url)
        data = response.json()
        self.destination_data = data['prices']
        return self.destination_data

    def update_destination_codes(self):
        # Use the Sheety API to go through each row of cities and update iataCode.
        for city in self.destination_data:
            new_data = {
            "price": {
                'iataCode': city['iataCode']
            }
            }
            #editing each row in sheet
            response = requests.put(url=f"{sheety_url}/{city['id']}",json=new_data)

            print(response.text)
