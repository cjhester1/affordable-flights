# main file, uses the DataManager,FlightSearch, FlightData, NotificationManager classes.
from data_manager import DataManager

data_manager = DataManager()

sheet_data = data_manager.get_destination_data()
print(sheet_data)

#check if sheet_data contains any values for the "iataCode" key.
#  If not, then the IATA Codes column is empty in the Google Sheet.
#  In this case, pass each city name in sheet_data one-by-one
#  to the FlightSearch class to get the corresponding IATA code
#  for that city using the Flight Search API.
#  use the return value to update the sheet_data dictionary.
for row in sheet_data:
    if row['iataCode'] == "":
        print("missing iataCode.")
        from flight_search import FlightSearch
        search_flight = FlightSearch()
        row['iataCode'] = search_flight.get_destination_code(row["city"])


print(sheet_data)
data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

