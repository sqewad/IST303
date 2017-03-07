from datetime import datetime
import json

class Services(object):
    def __init__(self, service_name, capacity, charge_per_min, choice_of_length, schedule):
        self.service_name = service_name
        self.capacity = capacity
        self.charge_per_min = charge_per_min
        self.choice_of_length = choice_of_length
        self.schedule = schedule

    def edit_schedule(self, service_record, edit):
        if edit == 'add':
            self.schedule.append(service_record)
        elif edit == 'del':
            self.schedule.remove(service_record)
        json.dump(self.schedule, open('services_schedules/' + self.service_name + '.txt', 'w'))

    def check_service_schedule(self, start_time, end_time):
        count = 0
        for i in self.schedule:
            if datetime.strptime(i['start_time'], "%m/%d/%Y %H:%M") \
               < end_time and start_time \
               < datetime.strptime(i['end_time'], "%m/%d/%Y %H:%M"):
                count += 1
        if count < self.capacity:
            return True
        else: return False

    def charge(self, length_of_service):
        return self.charge_per_min * length_of_service
       