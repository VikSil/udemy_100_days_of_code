import sys
from data_manager import DataManager  # Sheety
from flight_data import FlightData  # Data Wrangler, calls other APIs
from notification_manager import NotificationManager  # Twilio
from user_acquisition import NewUser


def main():

    print('Please wait for the program to initialise...')

    # initialise data wrangler
    spreadsheet = DataManager()

    try:
        init_flights = spreadsheet.get_destination_data()
    except:
        print('Could not retrieve destination data. Program will exit.')
    else:
        wrangler = FlightData(init_flights)

        # find any missing airport codes and update the spreadsheet
        codes_to_update = wrangler.find_codes()
        if codes_to_update is not None:
            spreadsheet.update_rows(codes_to_update)

        # register the user
        is_new_user = input('Are you a new user signing up? (Y/N) ')
        if is_new_user == 'Y':
            new_user = NewUser()
            new_user.sign_up()
            try:
                spreadsheet.add_user(new_user.first_name, new_user.last_name, new_user.email)
            except:
                sys.exit('We could not sign you up, unfortunatelly. Program will exit.')
            else:
                print('You are in the club!')

        print('We are checking  for cheap flights and will send them out shortly...')
        print('Thank you for using our service.')

        # check for flights cheaper than in the spreadsheet
        cheapest_flights = wrangler.check_all_destinations()
        if len(cheapest_flights) > 0:

            # notify the default user via sms alerts
            notification_agent = NotificationManager()
            try:  # assume fault with service on first failure and don't attempt any more sms
                for flight in cheapest_flights:
                    notification_agent.send_sms_alert(flight['price'], flight['city'], flight['date'], flight['url'])
            except:
                print('Looks like sms notifications do not work right now')

            # notify all signed up users via email
            users = spreadsheet.get_user_data()
            for user in users:
                subject = f'{len(cheapest_flights)} cheap flights found for you!'
                text = f"Hi {user['firstName']}! \n\nThese are the low price flights we found for you:\n"
                for flight in cheapest_flights:
                    text += f"Only ${flight['price']} to fly from London to {flight['city']} on {flight['date']}. {flight['url']}\n"
                text += '\nAll the best,\nYour Cheap Flight Service'

                try:  # try emailing each user even if previous emails failed
                    notification_agent.send_email(user['email'], subject, text)
                except:
                    print('Might be a bit of an issue with the mailserver')


if __name__ == "__main__":
    main()
