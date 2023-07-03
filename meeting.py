import datetime
import pytz
import re


class Meeting:
    start = datetime.datetime.now(pytz.UTC)
    duration = 0
    location = "Offline Meeting"
    subject = ""
    uid = ""

    def __init__(self, appointment):
        self.start = appointment.start
        self.duration = int((appointment.end - appointment.start).total_seconds() // 60)
        self.subject = appointment.subject
        self.uid = appointment.uid

        # блок определения URL/локации встречи
        if appointment.location is not None and appointment.location.find("http") >= 0:
            self.location = appointment.location
        else:
            if appointment.location is not None:
                self.location = 'Offline meeting in ' + appointment.location
            text = appointment.body
            if text is None:
                text = 'empty'
                return
            meet_location = None
            compiled_re = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)",
                                     re.MULTILINE | re.UNICODE)
            urls = re.findall(compiled_re, text)
            for url in urls:
                if url[0].find('meet.') > 0:
                    meet_location = url[0]
                elif url[0].find('zoom.us') > 0:
                    meet_location = url[0]
                elif url[0].find('ktalk.') > 0:
                    meet_location = url[0]
            if meet_location is not None:
                self.location = meet_location.strip().replace('</a', '') #костыль для некоторых ktalk встреч

    def minutes_to_meeting(self):
        return int((self.start - datetime.datetime.now(pytz.utc)).total_seconds() // 60)

    def seconds_to_meeting(self):
        return int((self.start - datetime.datetime.now(pytz.utc)).total_seconds())

    def start_local(self, utc_pls):
        return self.start + datetime.timedelta(hours=utc_pls)

    def start_local_str(self, utc_plus):
        return (self.start + datetime.timedelta(hours=utc_plus)).strftime("%H:%M")
