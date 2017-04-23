import json
import os
from datetime import datetime, timedelta, date
from Guests import *
import Inputs
from Services import *
from Party_bills import *
from Rooms import *
from dateprocessing import *
from changeReservation import *


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
            json.dump(services[kind].schedule, open('services_schedules/' + kind + '.txt', 'w'), sort_keys=True, indent=4)
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
        json.dump(rooms[i].schedule, open('rooms_schedules/' + room_number + '.txt', 'w'), sort_keys=True, indent=4)
    else:
        rooms[i] = Rooms(room_number, size, json.load(open('rooms_schedules/' + room_number + '.txt', 'r')))


################################################################################################
################################################################################################
################################################################################################
################################################################################################



def register():
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
    party['status'] = ''

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
                json.dump(parties+[party], open('parties.txt', 'w'), sort_keys=True, indent=4)
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
        if guest_name in i['members'] and room_number in i['rooms'] and i['status'] in ['checkin', '']:
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
                    choice = input('please enter a number from 0 ~ 1): ')
                    print('-------------------------------------------------------------')
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
            print('the guest has booked another service for that time' +'\n'
                  'or try to book mineral bath within 2 hours')
            print('-------------------------------------------------------------')
        if services[service].check_service_schedule(start_time, end_time) is False:
            print('-------------------------------------------------------------')
            print('can\'t book')
            print('service schedule not available')
            print('-------------------------------------------------------------')

### we may need a fuction shows when the service is avalaible

def get_information_for_service():
    global services
    time_of_canceling = datetime.now()
    guest_name = input('guest\'s name: ')
    room_number = input('room number: ')
    guests = json.load(open('guests.txt', 'r'))
    parties = json.load(open('parties.txt', 'r'))
    for i in parties:
        if guest_name in i['members'] and room_number in i['rooms'] and i['status'] in ['', 'checkin']:
            party_id = i['party_id']
            break
    else:
        print('-------------------------------------------------------------')
        print('chech the guest\'s information, and try again!')
        print('-------------------------------------------------------------')
        raise ValueError
    for i in guests:
        if party_id == i['party_id'] and guest_name == i['guest_name']:
            guest_id = i['guest_id']
            break
    else:
        print('-------------------------------------------------------------')
        print('chech the guest\'s information, and try again!')
        print('-------------------------------------------------------------')
        raise ValueError

    while True:
        service = Inputs.service()
        date_time_string, start_time = Inputs.service_date_time()
        tag = 0
        for i in services[service].schedule:
            if i['guest_id'] == guest_id and i['start_time'] == date_time_string:
                time_of_reserving = i['time_of_reserving']
                tag = 1
                break
        else:
            print('-------------------------------------------------------------')
            print('no such reservation, check again')
        if tag == 1:
            break
    print('-------------------------------------------------------------')
    return guest_id, guest_name, party_id, service, time_of_reserving, time_of_canceling, start_time,date_time_string

def cancel_service(guest_id, guest_name, party_id, service, start_time, date_time_string, refund):
    global services
    schedule = json.load(open('guests_schedules/'+guest_id+'.txt', 'r'))
    party_bills = json.load(open('parties_bills/'+party_id+'.txt', 'r'))
    the_guest = Guests(guest_name, guest_id, party_id, schedule)

    for i in services[service].schedule:
        if i['guest_id'] == guest_id and i['start_time'] == date_time_string:
            services[service].edit_schedule(i, 'del')
            break
    for i in the_guest.schedule:
        if i['start_time'] == date_time_string:
            the_guest.edit_schedule(i, 'del')
            break
    for i in range(len(party_bills)):
        if party_bills[i]['guest_name'] == guest_name and party_bills[i]['date_time'] == date_time_string:
            party_bills[i]['item'] += ' (canceled)'
            party_bills[i]['charge'] *= 1 - refund
            json.dump(party_bills, open('parties_bills/' + party_id + '.txt', 'w'), sort_keys=True, indent=4)
            break
    print(guest_name, service, date_time_string, 'canceled')
    print('-------------------------------------------------------------')
    return

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
            print('please enter a number from 0 ~ 16')
            print('-------------------------------------------------------------')
    while True:
        try:
            n_double = int(input('how many double rooms the guest need: '))
            break
        except ValueError:
            print('-------------------------------------------------------------')
            print('please enter a number from 0 ~ 16')
            print('-------------------------------------------------------------')
    while True:
        try:
            n_quadruple = int(input('how many quadruple rooms the guest need: '))
            break
        except ValueError:
            print('-------------------------------------------------------------')
            print('please enter a number from 0 ~ 4')
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
        json.dump(parties, open('parties.txt', 'w'), sort_keys=True, indent=4)
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

def check_in():
    today_date = datetime.now()
    guest_name = input('guest\'s name: ')
    phone_number = input('phone number: ')
    parties = json.load(open('parties.txt', 'r'))
    for i in range(len(parties)):
        if guest_name in parties[i]['members'] and\
           phone_number == parties[i]['phone_number'] and\
           parties[i]['status'] == '' and\
           datetime.strptime(parties[i]['checkin_date'], "%m/%d/%Y") <= today_date:
            parties[i]['status'] = 'checkin'
            break
        elif guest_name in parties[i]['members'] and\
             phone_number == parties[i]['phone_number'] and\
             parties[i]['status'] == 'checkin':
            print('-------------------------------------------------------------')
            print('have already checked in')
            print('-------------------------------------------------------------')
            return
        else:
            print('-------------------------------------------------------------')
            print('check the information again!')
            print('-------------------------------------------------------------')
            return
    json.dump(parties, open('parties.txt', 'w'), sort_keys=True, indent=4)
    print('-------------------------------------------------------------')
    print('check in successfully!')
    print('room number: ' + ', '.join(x for x in parties[i]['rooms']))
    print('-------------------------------------------------------------')


def check_out():
    guest_name = input('guest\'s name: ')
    room_number = input('room number: ')
    parties = json.load(open('parties.txt', 'r'))
    for i in range(len(parties)):
        if guest_name in parties[i]['members'] and\
           room_number in parties[i]['rooms'] and\
           parties[i]['status'] == 'checkin':
            parties[i]['status'] = 'checkout'
            break
    else:
        print('check the information again!')
        return
    json.dump(parties, open('parties.txt', 'w'), sort_keys=True, indent=4)
    print('-------------------------------------------------------------')
    print('check out successfully!')
    print('-------------------------------------------------------------')


def show_services_schedule():
    kind = Inputs.service()
    the_date = Inputs.input_date()
    schedule_raw = services[kind].schedule
    schedule = []
    for i in schedule_raw:
        start_time = datetime.strptime(i['start_time'], "%m/%d/%Y %H:%M")
        end_time = datetime.strptime(i['end_time'], "%m/%d/%Y %H:%M")
        period = Datetimeperiod(start_time, end_time, 1)
        schedule.append(period)
    newschedule = schedule_new([], schedule)
    unavailable = []
    unavailable_in_that_day = []
    for i in newschedule:
        if i.count == services[kind].capacity:
            start_time = i.start_time
            end_time = i.end_time
            record = {'start_time': start_time, 'end_time': end_time}
            unavailable.append(record)
    for i in unavailable:
        if i['start_time'].date() == the_date and i['end_time'].date() == the_date:
            unavailable_in_that_day.append(i)
        elif i['start_time'].date() < the_date and i['end_time'].date() == the_date:
            record = {'start_time': datetime.combine(the_date, datetime.min.time()),\
                      'end_time': i['end_time']}
            unavailable_in_that_day.append(record)
        elif i['start_time'].date() == the_date and i['end_time'].date() > the_date:
            record = {'end_time': datetime.combine(the_date, datetime.max.time()),\
                      'start_time': i['start_time']}
            unavailable_in_that_day.append(record)
    return unavailable_in_that_day

def show_guest_schedule_from_now():
    guest_name = input('guest\'s name: ')
    room_number = input('room number: ')
    guests = json.load(open('guests.txt', 'r'))
    parties = json.load(open('parties.txt', 'r'))
    for i in parties:
        if guest_name in i['members'] and room_number in i['rooms'] and i['status'] != 'checkout':
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
    schedule = json.load(open('guests_schedules/'+guest_id+'.txt', 'r'))
    new_schedule = []
    for i in schedule:
        start_time = datetime.strptime(i['start_time'], "%m/%d/%Y %H:%M")
        now = datetime.now()
        if start_time >= now():
            new_schedule.append(i)
    print(new_schedule)


def get_info_for_room_cancelation():
    now = datetime.now()
    guests = json.load(open('guests.txt', 'r'))
    parties = json.load(open('parties.txt', 'r'))
    guest_name = input('guest\'s name: ')
    phone_number = input('phone number: ')
    for i in parties:
        if guest_name in i['members'] and phone_number == i['phone_number'] and i['status'] == '':
            party_id = i['party_id']
            checkin_date_string = i['checkin_date']
            # checkout_date_string = i['checkout_date']
            room_list = i['rooms']
            index = parties.index(i)
            break
    else:
        print('-------------------------------------------------------------')
        print('check the guest\'s information, and try again!')
        print('-------------------------------------------------------------')
        raise ValueError
    checkin_date = datetime.strptime(checkin_date_string, "%m/%d/%Y")
    return guests, parties, party_id, now, checkin_date, room_list, index

def cancel_room(parties, party_id, now, checkin_date, room_list, index, refund):
    global rooms
    party_bills = json.load(open('parties_bills/' + party_id + '.txt', 'r'))
    for i in room_list:
        for record in rooms[int(i)].schedule:
            if record['party_id'] == party_id:
                rooms[int(i)].edit_schedule(record, 'del')
            for j in range(len(party_bills)):
                if party_bills[j]['item'] == rooms[int(i)].size + ' room':
                    party_bills[j]['item'] += ' (canceled)'
                    party_bills[j]['charge'] *= 1-refund
    json.dump(party_bills, open('parties_bills/' + party_id + '.txt', 'w'), sort_keys=True, indent=4)

    parties[index]['status'] = 'canceled'
    json.dump(parties, open('parties.txt', 'w'), sort_keys=True, indent=4)
    print('cancel room successfully!')
    print('-------------------------------------------------------------')


def shortern_the_stay(): # at least check-in for one night
    pass



################################################################################################
################################################################################################
################################################################################################
################################################################################################


#main menu
while True:
    while True:
        print('1. reserve room'+'\n'
              '2. cancel room'+'\n'
              '3. reserve service'+'\n'
              '4. cancel service'+'\n'
              '5. check in'+'\n'
              '6. check out'+'\n'
              '7. edit reservation'+'\n'
              '0. exit')
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
        # cancel service first
        try:
            guests, parties, party_id, now, checkin_date, room_list, index = get_info_for_room_cancelation()
        except ValueError:
            continue
        time_of_canceling = now
        if checkin_date - now >= timedelta(21): # cancel before 3 weeks
            print('-------------------------------------------------------------')
            print('you can get 100% refund for rooms')
            room_refund = 1
        elif checkin_date - now >= timedelta(2): # cancel before 48 hours
            print('-------------------------------------------------------------')
            print('you can only get 75% refund for rooms')
            room_refund = 0.75
        else: # less than 48 hours
            print('-------------------------------------------------------------')
            print('no refund for rooms!!')
            room_refund = 0
        if Inputs.cancel_confirm():
            print('-------------------------------------------------------------')
            print('befor room cancelation, you have to cancel all the services first')
            if Inputs.cancel_confirm():
                print('-------------------------------------------------------------')
                for guest in guests:
                    if guest['party_id'] == party_id:
                        guest_id = guest['guest_id']
                        guest_name = guest['guest_name']
                        guest_schedule = json.load(open('guests_schedules/'+guest_id+'.txt', 'r'))
                        for record in guest_schedule:
                            service = record['service']
                            date_time_string = record['start_time']
                            start_time = datetime.strptime(date_time_string, "%m/%d/%Y %H:%M")
                            time_of_reserving_string = record['time_of_reserving']
                            if (start_time - time_of_canceling >= timedelta(0, 90 * 60)) or \
                            (time_of_canceling - datetime.strptime(time_of_reserving_string, "%m/%d/%Y %H:%M") \
                            <= timedelta(0, 10 * 60)):
                                service_refund = 1
                            else:
                                service_refund = 0
                            cancel_service(guest_id, guest_name, party_id, service, start_time, date_time_string, service_refund)

                cancel_room(parties, party_id, now, checkin_date, room_list, index, room_refund)

    elif num == 3:
        reserve_service()
    elif num == 4:
        try:
            guest_id, guest_name, party_id, service, time_of_reserving, time_of_canceling, start_time, date_time_string = get_information_for_service()
        except ValueError:
            continue

        if (start_time - time_of_canceling >= timedelta(0, 90 * 60)) or \
        (time_of_canceling - datetime.strptime(time_of_reserving, "%m/%d/%Y %H:%M") \
        <= timedelta(0, 10 * 60)):
            print('can cancel without getting charged')
            refund = 1
        else:
            print('can cancel, but will still get charged')
            refund = 0

        if Inputs.cancel_confirm():
            print('-------------------------------------------------------------')
            cancel_service(guest_id, guest_name, party_id, service, start_time, date_time_string, refund)
    elif num == 5:
        check_in()
    elif num == 6:
        check_out()
    elif num == 7:
        time_of_canceling = datetime.now()
        guests, parties, party_id, checkin_date, checkout_date, roomsnum, index, days, cancel_date_str_list = get_info_for_shorten_stay()
        print('-------------------------------------------------------------')
        print('befor re-schedule rooms, you have to cancel the services during that time')
        if Inputs.cancel_confirm():
            print('-------------------------------------------------------------')
            for guest in guests:
                if guest['party_id'] == party_id:
                    guest_id = guest['guest_id']
                    guest_name = guest['guest_name']
                    guest_schedule = json.load(open('guests_schedules/'+guest_id+'.txt', 'r'))
                    for record in guest_schedule:
                        if record['start_time'][:10] in cancel_date_str_list:
                            service = record['service']
                            date_time_string = record['start_time']
                            start_time = datetime.strptime(date_time_string, "%m/%d/%Y %H:%M")
                            time_of_reserving_string = record['time_of_reserving']
                            if (start_time - time_of_canceling >= timedelta(0, 90 * 60)) or \
                            (time_of_canceling - datetime.strptime(time_of_reserving_string, "%m/%d/%Y %H:%M") \
                            <= timedelta(0, 10 * 60)):
                                service_refund = 1
                            else:
                                service_refund = 0
                            cancel_service(guest_id, guest_name, party_id, service, start_time, date_time_string, service_refund)

            changeReservation(rooms, guests, parties, party_id, checkin_date, checkout_date, roomsnum, index, days, cancel_date_str_list)
    elif num == 0:
        break


