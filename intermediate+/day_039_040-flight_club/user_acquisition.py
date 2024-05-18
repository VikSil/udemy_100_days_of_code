class NewUser:

    def __init__(self):
        self.first_name = ''
        self.last_name = ''
        self.email = ''

    def sign_up(self):
        print('Welcome to Angela\'s Flight Club.')
        print('We will find the best flight deals and email them to you.')
        self.first_name = input('What is your first name? ')
        self.last_name = input('What is your last name? ')
        got_email = False
        while not got_email:
            email1 = input('What is your email? ')
            email2 = input('Please type your email again. ')
            if email1 == email2:
                got_email = True
                self.email = email1
            else:
                print('The two emails don\'t match. Please try again.')
