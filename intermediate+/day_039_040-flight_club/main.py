from data_manager import DataManager  # Sheety
from flight_data import FlightData  # Data Wrangler, calls other APIs


def main():

    spreadsheet = DataManager()
    init_flights = spreadsheet.get_all_data()

    wrangler = FlightData(init_flights)
    codes_to_update = wrangler.find_codes()

    if codes_to_update is not None:
        spreadsheet.update_rows(codes_to_update)

    wrangler.check_all_destinations()


if __name__ == "__main__":
    main()
