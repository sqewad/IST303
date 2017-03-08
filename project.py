import json
import os
from datetime import datetime
from datetime import timedelta
from Guests import *
import Inputs
from Services import *
from Party_bills import *
from Rooms import *


# create folders
os.makedirs(os.path.dirname('services_schedules/'), exist_ok=True)
os.makedirs(os.path.dirname('guests_schedules/'), exist_ok=True)
os.makedirs(os.path.dirname('parties_bills/'), exist_ok=True)
os.makedirs(os.path.dirname('rooms_schedules/'), exist_ok=True)

# [[service_names],[capacity, price per min, choice of length]]
mineral_bath_list = [['mineral_bath'], [12, 2.5, [60, 90]]]
massage_list = [['massage_swedish', 'massage_shiatsu', 'massage_deep_tissue'], [4, 3.0, [30, 60]]]
facial_list = [['facial_normal', 'facial_collagen'], [3, 2.0, [30, 60]]]
specialty_treatment_list = [['specialty_treatment_hot_stone', \
                             'specialty_treatment_sugar_scrub', \
                             'specialty_treatment_herbal_body_wrap', \
                             'specialty_treatment_botanical_mud_wrap'], \
                             [2, 3.5, [60, 90]]]

services_list = [mineral_bath_list, massage_list, facial_list, specialty_treatment_list]
services = {}

for service in services_list:
    for kind in service[0]:
        if not os.path.isfile('services_schedules/' + kind + '.txt'):
            services[kind] = Services(kind, service[1][0], service[1][1], service[1][2], [])
            json.dump(services[kind].schedule, open('services_schedules/' + kind + '.txt', 'w'))
        else:
            services[kind] = Services(kind, service[1][0], service[1][1], service[1][2], \
            json.load(open('services_schedules/' + kind + '.txt', 'r')))
 # rooms
rooms = {}
for i in range(36):
    if i < 16:
        size = 'single'
    elif 16 <= i < 32:
        size = 'double'
    else:
        size = 'quadruple'
    room_number = ('0'*3 + str(i))[-3:]
    if not os.path.isfile('rooms_schedules/' + room_number + '.txt'):
        rooms[i] = Rooms(room_number, size, [])
        json.dump(rooms[i].schedule, open('rooms_schedules/' + room_number + '.txt', 'w'))
    else:
        rooms[i] = Rooms(room_number, size, json.load(open('rooms_schedules/' + room_number + '.txt', 'r')))


################################################################################################
################################################################################################
################################################################################################
################################################################################################



def register():
    global services
    party = {}
    if os.path.exists('parties.txt'):
        parties = json.load(open('parties.txt', 'r'))
        party_id = str(len(parties))
    else:
        parties = []
        party_id = '0'
    party['party_id'] = party_id
    party['members'] = []
    party['rooms'] = []
    party['checkin_date'] = ''
    party['checkout_date'] = ''

    while True:
        guest_name = input('guest\'s name: ')
        if os.path.exists('guests.txt'):
            guests = json.load(open('guests.txt', 'r'))
            guest_id = str(len(guests))
        else:
            guests = []
            guest_id = '0'
        party['members'].append(guest_name)
        new_guest = Guests(guest_name, guest_id, party_id, [])
        new_guest.creat_schedule_file()
        new_guest.add_guest_to_guests(guests)
        print('guest added')
        print('-------------------------------------------------------------')

        while True:
            group = input('any other group members? Y/N ')
            if group == 'Y' or group == 'y' or group == 'yes':
                print('-------------------------------------------------------------')
                print('continue')
                print('-------------------------------------------------------------')
                break
            elif group == 'N' or group == 'n' or group == 'no':
                new_party_bills = Party_bills(party['party_id'], [])
                new_party_bills.creat_party_bills_file()
                party['phone_number'] = input('phone number: ')
                json.dump(parties+[party], open('parties.txt', 'w'))
                print('-------------------------------------------------------------')
                print('add party successfully')
                print('-------------------------------------------------------------')
                return 
            else:
                print('-------------------------------------------------------------')
                print('type again. Y/N ')
                print('-------------------------------------------------------------')


def reserve_service():
    global services
    time_of_reserving = datetime.now().strftime('%m/%d/%Y %H:%M') # for cancelation
    guest_name = input('guest\'s name: ')
    room_number = input('room number: ')
    guests = json.load(open('guests.txt', 'r'))
    parties = json.load(open('parties.txt', 'r'))
    for i in parties:
        if guest_name in i['members'] and room_number in i['rooms']:
            party_id = i['party_id']
            checkin_date_string = i['checkin_date']
            checkout_date_string = i['checkout_date']
            break
    else:
        print('-------------------------------------------------------------')
        print('chech the guest\'s information, and try again!')
        print('-------------------------------------------------------------')
        return
    for i in guests:
        if party_id == i['party_id'] and guest_name == i['guest_name']:
            guest_id = i['guest_id']
            break
    else:
        print('-------------------------------------------------------------')
        print('chech the guest\'s information, and try again!')
        print('-------------------------------------------------------------')
        return

    service = Inputs.service()

    while True:
        date_time_string, start_time = Inputs.service_date_time()
        if start_time >= datetime.now():
            if datetime.strptime(checkin_date_string, "%m/%d/%Y") + timedelta(0, 15*3600) > start_time or \
               datetime.strptime(checkout_date_string, "%m/%d/%Y") + timedelta(0, 12*3600) <= start_time:
                while True:
                    print('-------------------------------------------------------------')
                    print('0. please reserve room for that time first or' + '\n'
                          '1. change the service time')
                    choice = input('enter a number (0 or 1): ')
                    if choice == '0':
                        return
                    elif choice == '1':
                        break
                    else:
                        print('-------------------------------------------------------------')
                        print('please enter 0 or 1')
            else:
                break
        else:
            print('-------------------------------------------------------------')
            print('please enter a time later than now')

    length_of_service = Inputs.length_of_service(service, services)

    end_time = start_time + timedelta(0, length_of_service * 60)

    service_record = {'start_time':date_time_string, 'end_time':end_time.strftime('%m/%d/%Y %H:%M'),
                      'time_of_reserving':time_of_reserving, 'guest_name': guest_name,
                      'guest_id':guest_id}
    guest_record = {'start_time':date_time_string, 'end_time':end_time.strftime('%m/%d/%Y %H:%M'),
                    'time_of_reserving':time_of_reserving, 'service':service}

    schedule = json.load(open('guests_schedules/'+guest_id+'.txt', 'r'))
    the_guest = Guests(guest_name, guest_id, party_id, schedule)

    if service != 'mineral_bath':
        guest_available = the_guest.check_guest_schedule(start_time, end_time)
    else: # service == 'mineral_bath'
        guest_available = the_guest.check_mineral_bath(start_time, end_time)
    if guest_available and services[service].check_service_schedule(start_time, end_time):
        the_guest.edit_schedule(guest_record, 'add')
        services[service].edit_schedule(service_record, 'add')
        charge = services[service].charge(length_of_service)
        record = {'date_time': date_time_string, 'guest_name': guest_name,
                  'item': service, 'charge': charge}
        party_bills = json.load(open('parties_bills/' + party_id + '.txt', 'r'))
        the_party_bills = Party_bills(party_id, party_bills)
        the_party_bills.edit_party_bills(record, 'add')
        print('-------------------------------------------------------------')
        print('book successfully')
        print('-------------------------------------------------------------')
    else:
        if guest_available is False:
            print('-------------------------------------------------------------')
            print('can\'t book')
            print('the guest has booked another service for that time \
                  or try to book mineral bath within 2 hours')
            print('-------------------------------------------------------------')
        if services[service].check_service_schedule(start_time, end_time) is False:
            print('-------------------------------------------------------------')
            print('can\'t book')
            print('service schedule not available')
            print('-------------------------------------------------------------')

### we may need a fuction shows when the service is avalaible

def cancel_service():
    global services
    time_of_canceling = datetime.now()
    guest_name = input('guest\'s name: ')
    room_number = input('room number: ')
    guests = json.load(open('guests.txt', 'r'))
    parties = json.load(open('parties.txt', 'r'))
    for i in parties:
        if guest_name in i['members'] and room_number in i['rooms']:
            party_id = i['party_id']
            break
    else:
        print('-------------------------------------------------------------')
        print('chech the guest\'s information, and try again!')
        print('-------------------------------------------------------------')
        return
    for i in guests:
        if party_id == i['party_id'] and guest_name == i['guest_name']:
            guest_id = i['guest_id']
            break
    else:
        print('-------------------------------------------------------------')
        print('chech the guest\'s information, and try again!')
        print('-------------------------------------------------------------')
        return

    service = Inputs.service()
    date_time_string, start_time = Inputs.service_date_time()

    for i in services[service].schedule:
        if i['guest_id'] == guest_id and i['start_time'] == date_time_string:
            time_of_reserving = i['time_of_reserving']
            break
    else:
        print('-------------------------------------------------------------')
        print('no such reservation, check again')
        print('-------------------------------------------------------------')
        return

    if (start_time - time_of_canceling >= timedelta(0, 90 * 60)) or \
       (time_of_canceling - datetime.strptime(time_of_reserving, "%m/%d/%Y %H:%M") \
       <= timedelta(0, 10 * 60)):
        print('-------------------------------------------------------------')
        print('can cancel without getting charged')
        charge = False
    else:
        print('-------------------------------------------------------------')
        print('can cancel, but will still get charged')
        charge = True
    print('still wanna cancel?')
    while True:
        confirm = input('0. dont\'t cancel' + '\n'
                        '1. cancel' + '\n'
                        'enter the number: ')
        if confirm == '0':
            print('-------------------------------------------------------------')
            print('no cancelation!')
            return
        elif confirm == '1':
            schedule = json.load(open('guests_schedules/'+guest_id+'.txt', 'r'))
            party_bills = json.load(open('parties_bills/'+party_id+'.txt', 'r'))
            the_guest = Guests(guest_name, guest_id, party_id, schedule)
            the_party_bills = Party_bills(party_id, party_bills)

            for i in services[service].schedule:
                if i['guest_id'] == guest_id and i['start_time'] == date_time_string:
                    services[service].edit_schedule(i, 'del')
                    break
            for i in the_guest.schedule:
                if i['start_time'] == date_time_string:
                    the_guest.edit_schedule(i, 'del')
                    break
            if charge is False:
                for i in party_bills:
                    if i['guest_name'] == guest_name and i['date_time'] == date_time_string:
                        the_party_bills.edit_party_bills(i, 'del')
                        break
            print('-------------------------------------------------------------')
            print('canceled')
            print('-------------------------------------------------------------')
            return
        else:
            print('-------------------------------------------------------------')
            print('enter 0 or 1')
            print('-------------------------------------------------------------')

def reserve_room():
    global rooms

    parties = json.load(open('parties.txt', 'r'))

    index = len(parties) - 1
    party_id = str(index)
    guest_name = parties[index]['members'][0]

    checkin_date, checkout_date, checkin_date_string, checkout_date_string \
    = Inputs.check_in_out_date()

    days = (checkout_date - checkin_date).days
    while True:
        try:
            n_single = int(input('how many single rooms the guest need: '))
            break
        except ValueError:
            print('-------------------------------------------------------------')
            print('enter a number 0 ~ 16')
            print('-------------------------------------------------------------')
    while True:
        try:
            n_double = int(input('how many double rooms the guest need: '))
            break
        except ValueError:
            print('-------------------------------------------------------------')
            print('enter a number 0 ~ 16')
            print('-------------------------------------------------------------')
    while True:
        try:
            n_quadruple = int(input('how many quadruple rooms the guest need: '))
            break
        except ValueError:
            print('-------------------------------------------------------------')
            print('enter a number 0 ~ 4')
            print('-------------------------------------------------------------')
    #single room available
    single_count = 0
    single_list = []
    for i in range(16):
        if rooms[i].check_room_schedule(checkin_date, checkout_date):
            single_count += 1
            single_list.append(rooms[i].room_number)
    #double room available
    double_count = 0
    double_list = []
    for i in range(16, 32):
        if rooms[i].check_room_schedule(checkin_date, checkout_date):
            double_list.append(rooms[i].room_number)
            double_count += 1
    quadruple_count = 0
    quadruple_list = []
    for i in range(32, 36):
        if rooms[i].check_room_schedule(checkin_date, checkout_date):
            quadruple_list.append(rooms[i].room_number)
            quadruple_count += 1
    if single_count >= n_single and \
       double_count >= n_double and \
       quadruple_count >= n_quadruple:
        room_list = single_list[:n_single] + double_list[:n_double] + quadruple_list[:n_quadruple]
        parties[index]['rooms'] = room_list
        parties[index]['checkin_date'] = checkin_date_string
        parties[index]['checkout_date'] = checkout_date_string
        party_record = {'checkin_date': checkin_date_string, 'checkout_date': checkout_date_string,
                        'party_id': party_id}
        for i in room_list:
            rooms[int(i)].edit_schedule(party_record, 'add')
            for j in range(days):
                date = checkin_date + timedelta(j)
                charge = rooms[int(i)].charge(date)
                bill_record = {'date_time': date.strftime('%m/%d/%Y'), 'guest_name': guest_name,
                               'item': rooms[int(i)].size + ' room', 'charge': charge}
                party_bills = json.load(open('parties_bills/' + party_id + '.txt', 'r'))
                the_party_bills = Party_bills(party_id, party_bills)
                the_party_bills.edit_party_bills(bill_record, 'add')
        json.dump(parties, open('parties.txt', 'w'))
        print('-------------------------------------------------------------')
        print('reserve successfully!')
        print('room number: ' + ', '.join(x for x in room_list))
        print('-------------------------------------------------------------')
        return True
    else:
        print('-------------------------------------------------------------')
        print('room not available at that time!')
        while True:
            continuing = input('try another date? y/n')
            if continuing == 'Y' or continuing == 'y' or continuing == 'yes':
                break
            elif continuing == 'N' or continuing == 'n' or continuing == 'no':
                return True
            else:
                print('-------------------------------------------------------------')
                print('type again. Y/N ')
                print('-------------------------------------------------------------')
        print('-------------------------------------------------------------')




def cancel_room():
    pass

################################################################################################
################################################################################################
################################################################################################
################################################################################################

while True:
    while True:
        print('1.reserve room'+'\n'
              '2.cancel room'+'\n'
              '3.reserve service'+'\n'
              '4.cancel service'+'\n'
              '0.exit')
        try:
            num = int(input('choose one: '))
            print('-------------------------------------------------------------')
            break
        except ValueError:
            print('-------------------------------------------------------------')
            print('please enter a number')
    if num == 1:
        register()
        while True:
            if reserve_room():
                break
    elif num == 2:
        cancel_room()
    elif num == 3:
        reserve_service()
    elif num == 4:
        cancel_service()
    elif num == 0:
        break


