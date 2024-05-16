import datetime
import pandas as pd
from flight_search import FlightSearch  # RapidAPI
from notification_manager import NotificationManager  # Twilio


class FlightData:

    def __init__(self, init_data):
        self.data = pd.DataFrame(init_data)
        self.location = 'LON'

    def find_codes(self):
        '''
        Function checks spreadsheet data for missing airport codes and retrieves codes from API
        Function returns a dictionary of rows wehre codes were missing with the codes filled in
        '''
        missing_code_rows = self.data.loc[self.data['iataCode'] == '']

        if not missing_code_rows.empty:
            missing_code_cities = missing_code_rows['city'].tolist()
            search_engine = FlightSearch()

            for city in missing_code_cities:
                airports = search_engine.get_airport_codes(city)
                code = airports[0]['id']  # first code in api reponse will be for all airports
                self.data.loc[(self.data['city'] == city) & (self.data['iataCode'] == ''), ['iataCode']] = code
                missing_code_rows.loc[
                    (missing_code_rows['city'] == city) & (missing_code_rows['iataCode'] == ''), ['iataCode']
                ] = code

            return missing_code_rows.to_dict(orient='records')  # if there were any missing codes, return updated rows
        return None

    def check_all_destinations(self):
        '''
        Function manages flight data requests, finds cheapest alternative and initiates alerts
        '''
        destinations = self.data.to_dict(orient='records')

        search_engine = FlightSearch()
        messanger = NotificationManager()

        for destination in destinations:  # for each destination in spreadsheet

            if (not isinstance(destination['dateFrom'], str)) or (
                destination['dateFrom'] == ''
            ):  # date range is not present
                date_from = datetime.date.today() + datetime.timedelta(days=1)
                date_to = datetime.date.today() + datetime.timedelta(days=5)
            else:  # date rnge is given in the spreadsheet
                date_from = datetime.datetime.strptime(destination['dateFrom'], '%Y-%m-%d')
                date_to = datetime.datetime.strptime(destination['dateTo'], '%Y-%m-%d')

            cheapest_url = ''
            max_price = int(destination['usdMaxPrice']) * 100
            flight_date = date_from

            while date_from <= date_to:  # for each date in range

                # find all flights that have prices less than that in the spreadsheet
                cheap_flights = search_engine.get_flights(
                    self.location, destination['iataCode'], date_from.strftime('%Y-%m-%d'), str(max_price)
                )
                for flight in cheap_flights:  # find the cheepest of the cheap flights
                    price = flight['travelerPrices'][0]['price']['price']['value']
                    ccy = flight['travelerPrices'][0]['price']['price']['currency']['code']
                    if ccy == 'USD' and price < max_price:
                        max_price = price
                        cheapest_url = flight['shareableUrl']
                        flight_date = date_from

                date_from += datetime.timedelta(days=1)

            if cheapest_url != '':  # a cheaper flight was found - send sms
                best_price = max_price / 100
                city = destination['city']
                date = flight_date.strftime('%Y-%m-%d')
                messanger.send_alert(best_price, city, date, cheapest_url)
