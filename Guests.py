from datetime import *
import json

class Guests(object):
    def __init__(self, guest_name, guest_id, party_id, schedule = []):
        self.guest_name = guest_name
        self.guest_id = guest_id
        self.party_id = party_id
        self.schedule = schedule
    
    def add_guest_to_guests(self, guests):
        temp = self.__dict__
        del temp['schedule']
        json.dump(guests+[temp],open('guests.txt','w'))

    def creat_schedule_file(self):
        json.dump(self.schedule,open('guests_schedules/' + self.guest_id + '.txt','w'))

    def edit_schedule(self, guest_record, edit):
        if edit == 'add':
            self.schedule.append(guest_record)
        elif edit == 'del':
            self.schedule.remove(guest_record)
        json.dump(self.schedule,open('guests_schedules/'+self.guest_id+'.txt','w'))

    def check_guest_schedule(self, start_time, end_time):
        for i in self.schedule:
            if datetime.strptime(i['start_time'], "%m/%d/%Y %H:%M") < end_time and \
               start_time < datetime.strptime(i['end_time'], "%m/%d/%Y %H:%M"):
                return False
        else: return True

    def check_mineral_bath(self, start_time, end_time):
        for i in self.schedule:
            if i['service'] == 'mineral_bath':
                if datetime.strptime(i['start_time'], "%m/%d/%Y %H:%M") - timedelta(0,2 * 3600) < end_time and \
                   start_time < datetime.strptime(i['end_time'], "%m/%d/%Y %H:%M") + timedelta(0,2 * 3600):
                    return False
        else: return True
