import time
from threading import Timer
import config
import texts
from meetbot import MeetBot
from meetings import Meetings


class Meeter:
    bot: MeetBot
    meetings: Meetings

    login = ""
    password = ""
    days_to_load = 1
    bot_api_token = ""
    bot_owner_id = 0

    prenotification_cache = []  # todo: сделать очистку кешей
    notification_cache = []

    load_meetings_timer: Timer
    load_meetings_timer_delay = config.LOAD_MEETING_TIMER_DELAY_SEC

    notification_timer: Timer
    notification_timer_delay = config.NOTIFICATION_TIMER_DELAY_SEC

    prenotify_delay_min = config.PRENOTIFY_DELAY_MINUTES
    utc_plus = config.LOCAL_UTC_PLUS

    def __init__(self, login, password, days_to_load, bot_api_token, bot_owner_id):
        self.login = login
        self.password = password
        self.bot_api_token = bot_api_token
        self.bot_owner_id = bot_owner_id
        self.days_to_load = days_to_load

        # предварительная очистика кешей. Без этого иногда креш
        self.prenotification_cache.clear()
        self.notification_cache.clear()

        # подготовка таймеров
        self.load_meetings_timer = Timer(config.LOAD_MEETING_TIMER_START_DELAY_SEC, self.on_load_meetings_timer_tick)
        self.load_meetings_timer.start()
        self.notification_timer = Timer(config.NOTIFICATION_TIMER_START_DELAY_SEC, self.on_notification_timer_tick)
        self.notification_timer.start()

        # подготовка календаря
        self.meetings = Meetings(login, password, days_to_load)

        # подготовка бота
        self.bot = MeetBot(self.bot_api_token, self.bot_owner_id)
        bot_thread = Timer(0, self.on_bot_started)
        bot_thread.start()

        self.bot.send_message(texts.BOT_STARTED_TEXT)

    def on_bot_started(self):
        while True:
            self.bot.go()

    def on_load_meetings_timer_tick(self):
        while True:
            print("Load meeting timer tick!")
            self.meetings.load_calendar()
            time.sleep(self.load_meetings_timer_delay)

    def on_notification_timer_tick(self):
        while True:
            print("Notification timer tick!")
            meetings = self.meetings.get_meetings()
            for meeting in meetings:
                # Проверяем ближайшие встречи
                if 0 < meeting.minutes_to_meeting() <= self.prenotify_delay_min:
                    try:
                        v = self.prenotification_cache.index(meeting.uid)
                    except ValueError:
                        self.prenotification_cache.append(meeting.uid)
                        self.prenotify_next_meeting(meeting)
                # Проверяем начавшиеся встречи
                if -31 <= meeting.seconds_to_meeting() <= 31:
                    try:
                        v = self.notification_cache.index(meeting.uid)
                    except ValueError:
                        self.notification_cache.append(meeting.uid)
                        self.notify_next_meeting(meeting)
            time.sleep(self.notification_timer_delay)

    def prenotify_next_meeting(self, meeting):
        self.bot.send_message(texts.PRENOTIFY_TEXT.format(
            min_to_meeting=str(meeting.minutes_to_meeting()),
            subject=meeting.subject,
            location=meeting.location
        ))

    def notify_next_meeting(self, meeting):
        self.bot.send_message(texts.NOTIFY_TEXT.format(
            start=meeting.start_local_str(self.utc_plus),
            subject=meeting.subject,
            location=meeting.location
        ))
