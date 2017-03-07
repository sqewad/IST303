from datetime import datetime
import json

class Rooms(object):
    def __init__(self, room_number, size, schedule):
        self.room_number = room_number
        self.size = size
        self.price = {'seasons':{'week_day':{'single':175, 'double':325, 'quadruple':600},
                                 'weekend' :{'single':205, 'double':355, 'quadruple':630}},
                      'off_seasons':{'week_day':{'single':140, 'double':260, 'quadruple':480},
                                     'weekend' :{'single':170, 'double':290, 'quadruple':510}}}
        self.schedule = schedule

    def check_room_schedule(self, checkin_date, checkout_date):
        for i in self.schedule:
            if datetime.strptime(i['checkin_date'], "%m/%d/%Y") < checkout_date and \
               checkin_date < datetime.strptime(i['checkout_date'], "%m/%d/%Y"):
                return False
        else: return True

    def edit_schedule(self, record, edit):
        if edit == 'add':
            self.schedule.append(record)
        elif edit == 'del':
            self.schedule.remove(record)
        # record = {'chechin_date': MM/DD/YYYY, 'checkout_date': MM/DD/YYYY, 'party_id'：'x'}
        json.dump(self.schedule, open('rooms_schedules/' + str(self.room_number) + '.txt', 'w'))

    def charge(self, date):
        if datetime(date.year, 1, 16) <= date <= datetime(date.year, 5, 14) or \
           datetime(date.year, 8, 16) <= date <= datetime(date.year, 12, 14):
            if date.isoweekday() <= 5:
                return self.price['off_seasons']['week_day'][self.size]
            else:
                return self.price['off_seasons']['weekend'][self.size]
        else:
            if date.isoweekday() <= 5:
                return self.price['seasons']['week_day'][self.size]
            else:
                return self.price['seasons']['weekend'][self.size]
            