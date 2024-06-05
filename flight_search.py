import os

import requests
from dotenv import load_dotenv
load_dotenv()

token_endpoint = os.getenv("TOKEN_ENDPOINT")
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"

class FlightSearch:
    #responsible for talking to Flight Search API

    def __init__(self):

        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_SECRET"]
        self._token = self._get_new_token()

    def _get_new_token(self):
        """
        Generates the authentication token used for accessing the Amadeus API and returns it.
        This function makes a POST request to the Amadeus token endpoint with the required
        credentials (API key and API secret) to obtain a new client credentials token.
        Upon receiving a response, the function updates the FlightSearch instance's token.
        Returns:
            str: The new access token obtained from the API response.
        """
        # Header with content type as per Amadeus documentation

        #code = "Testing"
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
        'grant_type': 'client_credentials',
        'client_id': self._api_key,
        'client_secret': self._api_secret
        }
        response = requests.post(url=token_endpoint, headers=header, data=body)
        testme = response.json()
        # New bearer token. Typically expires in 1799 seconds (30min)
        print(f"Your token is {testme}")
       # print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']


    def get_destination_code(self,city):
        """
            Retrieves the IATA code for a specified city using the Amadeus Location API.
            Parameters:
            city_name (str): The name of the city for which to find the IATA code.
            Returns:
            str: The IATA code of the first matching city if found; "N/A" if no match is found due to an IndexError,
            or "Not Found" if no match is found due to a KeyError.

            The function sends a GET request to the IATA_ENDPOINT with a query that specifies the city
            name and other parameters to refine the search. It then attempts to extract the IATA code
            from the JSON response.
            - If the city is not found in the response data (i.e., the data array is empty, leading to
            an IndexError), it logs a message indicating that no airport code was found for the city and
            returns "N/A".
            - If the expected key is not found in the response (i.e., the 'iataCode' key is missing, leading
            to a KeyError), it logs a message indicating that no airport code was found for the city
            and returns "Not Found".
            """
        body = {
        "keyword": city,
        "max": "2",
        "include":"AIRPORTS"

        }
        print(f"using this --> {self._token} to get a new token")
        headers = {"Authorization": f"Bearer {self._token}"}
        response = requests.get(url=IATA_ENDPOINT, headers=headers,params=body)
        try:
            code = response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"No airport iataCode found for {city}")
            return "Not found, index error"
        except KeyError:
            print(f"No airport iataCode found for {city}")
            return "Not found, Key error"

        return code
