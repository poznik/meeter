import datetime
import pytz
from exchangelib import Credentials, Account
from meeting import Meeting


class Meetings:
    login = ""
    password = ""
    days_to_load = 1
    cache = []

    def __init__(self, login, password, days_to_load):
        self.login = login
        self.password = password
        self.days_to_load = days_to_load

    def load_calendar(self):
        print("Starting load appointments...")
        credentials = Credentials(self.login, self.password)
        account = Account(self.login, credentials=credentials, autodiscover=True)
        start = datetime.datetime.now(pytz.UTC)
        end = datetime.datetime.now(pytz.UTC) + datetime.timedelta(days=self.days_to_load)
        all_meetings = account.calendar.view(start=start, end=end)
        self.cache.clear()
        for itm in all_meetings:
            self.cache.append(Meeting(itm))
        print("Loaded: " + str(len(self.cache)) + " appointments")

    def get_meetings(self):
        return self.cache
