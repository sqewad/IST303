import json
import os
from datetime import *
from Guests import *
import Inputs
from Services import *
from Party_bills import *
from Rooms import *

print('there are 3 functions:'+'\n'
        'register()'+'\n'
        'reserve_service()'+'\n'
        'cancel_service()')


# create folders
os.makedirs(os.path.dirname('services_schedules/'), exist_ok=True)
os.makedirs(os.path.dirname('guests_schedules/'), exist_ok=True)
os.makedirs(os.path.dirname('parties_bills/'), exist_ok=True)
os.makedirs(os.path.dirname('rooms_schedules/'), exist_ok=True)

# [[service_names],[capacity, price per min, choice of length]]
mineral_bath_list = [['mineral_bath'],[12, 2.5, [60, 90]]]
massage_list = [['massage_swedish', 'massage_shiatsu', 'massage_deep_tissue'],[4, 3.0, [30, 60]]]
facial_list = [['facial_normal', 'facial_collagen'],[3, 2.0, [30, 60]]]
specialty_treatment_list = [['specialty_treatment_hot_stone', 'specialty_treatment_sugar_scrub', 'specialty_treatment_herbal_body_wrap', 'specialty_treatment_botanical_mud_wrap'],
                        [2, 3.5, [60, 90]]]

services_list = [mineral_bath_list, massage_list, facial_list, specialty_treatment_list]
services = {}

for service in services_list:
    for kind in service[0]:
        if not os.path.isfile('services_schedules/' + kind + '.txt'):
            services[kind] = Services(kind, service[1][0], service[1][1], service[1][2], [])
            json.dump(services[kind].schedule,open('services_schedules/' + kind + '.txt','w'))
        else:
            services[kind] = Services(kind, service[1][0], service[1][1], service[1][2], json.load(open('services_schedules/' + kind + '.txt','r')))
 # rooms 
rooms = {}
for i in range(36):
    if i < 16:
        size = 'single'
    elif 16 <= i < 32:
        size = 'double'
    else:
        size = 'quadruple'
    if not os.path.isfile('rooms_schedules/' + str(i) + '.txt'):
        rooms[i] = Rooms(i, size)
        json.dump(rooms[i].schedule,open('rooms_schedules/' + str(i) + '.txt','w'))
    else:
        rooms[i] = Rooms(i, size, json.load(open('rooms_schedules/' + str(i) + '.txt','r')))


################################################################################################
################################################################################################
################################################################################################
################################################################################################



def register():
    global services
    party = {}
    if os.path.exists('parties.txt'):
        parties = json.load(open('parties.txt','r'))
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
            guests = json.load(open('guests.txt','r'))
            guest_id = str(len(guests))
        else:
            guests = [] 
            guest_id = '0'
        party['members'].append(guest_name)
        new_guest = Guests(guest_name,guest_id,party_id)
        new_guest.creat_schedule_file()
        new_guest.add_guest_to_guests(guests)
        
        while True:
            group = input('any other group members? Y/N ')
            if group == 'Y' or group == 'y' or group =='yes':
                print('-------------------------------------------------------------') 
                print('continue')
                print('-------------------------------------------------------------') 
                break
            elif group =='N' or group =='n' or group =='no':
                new_party_bills = Party_bills(party['party_id'])
                new_party_bills.creat_party_bills_file()
                party['phone_number'] = input('phone number: ')
                json.dump(parties+[party],open('parties.txt','w'))
                print('-------------------------------------------------------------') 
                print('add guests successfully')
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
    guests = json.load(open('guests.txt','r'))
    parties = json.load(open('parties.txt','r'))
    for i in parties:
        if guest_name in i['members'] and room_number in i['rooms']:
            party_id = i['party_id']
            break
    else:
        print('-------------------------------------------------------------')
        print('chech the guest\'s information, and try again!')
        return
    for i in guests:
        if party_id == i['party_id'] and guest_name == i['guest_name']:
            guest_id = i['guest_id']
            break
    else:
        print('-------------------------------------------------------------')
        print('chech the guest\'s information, and try again!')
        return
        
    service = Inputs.service()
    
    while True:
        date_time, start_time = Inputs.service_date_time()
        if start_time >= datetime.now():
            break
        else:
            print('-------------------------------------------------------------') 
            print('please enter a time in the future')
    length_of_service = Inputs.length_of_service(service,services)
       
    end_time = start_time + timedelta(0,length_of_service * 60)
    
    service_record = {'start_time':date_time, 'end_time':end_time.strftime('%m/%d/%Y %H:%M'),
                      'time_of_reserving':time_of_reserving, 'guest_name': guest_name, 'guest_id':guest_id}
    guest_record = {'start_time':date_time, 'end_time':end_time.strftime('%m/%d/%Y %H:%M'),
                    'time_of_reserving':time_of_reserving, 'service':service}
    
    schedule = json.load(open('guests_schedules/'+guest_id+'.txt','r'))
    the_guest = Guests(guest_name, guest_id, schedule)
    
    if service != 'mineral_bath':
        guest_available = the_guest.check_guest_schedule(start_time, end_time)
    else: # service == 'mineral_bath'
        guest_available = the_guest.check_mineral_bath(start_time, end_time)
    if guest_available and services[service].check_service_schedule(start_time, end_time):
        the_guest.edit_schedule(guest_record,'add')
        services[service].edit_schedule(service_record,'add')
        charge = services[service].charge(length_of_service)
        record = {'date_time': date_time, 'guest_name': guest_name, 'service': service, 'charge': charge}
        party_bills = json.load(open('parties_bills/' + party_id + '.txt','r'))
        the_party_bills = Party_bills(party_id, party_bills)
        the_party_bills.edit_party_bills(record, 'add')
        print('-------------------------------------------------------------') 
        print('book successfully')
    else:
        if guest_available == False:
            print('-------------------------------------------------------------') 
            print('can\'t book')
            print('the guest has booked another service for that time or try to book mineral bath within 2 hours')
        if services[service].check_service_schedule(start_time, end_time) == False:
            print('-------------------------------------------------------------') 
            print('can\'t book')
            print('service schedule not available') 

### we may need a fuction shows when the service is avalaible

def cancel_service():
    global services
    time_of_canceling = datetime.now()
    guest_name = input('guest\'s name: ')
    guests = json.load(open('guests.txt','r'))
    parties = json.load(open('parties.txt','r'))
    # for i in guests:
    #     if i['guest_name'] == guest_name:
    #         guest_id = i['guest_id']
    #         party_id = i['party_id']
    #         break
    # else:
    #     print('-------------------------------------------------------------')
    #     print('chech the guest\'s information, and try again!')
    #     return

    for i in parties:
        if guest_name in i['members'] and room_number in i['rooms']:
            party_id = i['party_id']
            break
    else:
        print('-------------------------------------------------------------')
        print('chech the guest\'s information, and try again!')
        return
    for i in guests:
        if party_id == i['party_id'] and guest_name == i['guest_name']:
            guest_id = i['guest_id']
            break
    else:
        print('-------------------------------------------------------------')
        print('chech the guest\'s information, and try again!')
        return
        

    service = Inputs.service()
    date_time, start_time = Inputs.service_date_time()

    for i in services[service].schedule:
        if i['guest_id'] == guest_id and i['start_time'] == date_time:
            time_of_reserving = i['time_of_reserving']
            break
    else:
        print('-------------------------------------------------------------')
        print('no such reservation, check again')
        return
    
    if (start_time - time_of_canceling >= timedelta(0,90 * 60)) or \
       (time_of_canceling - datetime.strptime(time_of_reserving, "%m/%d/%Y %H:%M") <= timedelta(0,10 * 60)):
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
            schedule = json.load(open('guests_schedules/'+guest_id+'.txt','r'))
            party_bills = json.load(open('parties_bills/'+party_id+'.txt','r'))
            the_guest = Guests(guest_name, guest_id, party_id, schedule)
            the_party_bills = Party_bills(party_id,party_bills)

            for i in services[service].schedule:
                if i['guest_id'] == guest_id and i['start_time'] == date_time:
                    services[service].edit_schedule(i, 'del')
                    break
            for i in the_guest.schedule:
                if i['start_time'] == date_time:
                    the_guest.edit_schedule(i, 'del')
                    break
            if charge == False:
                for i in party_bills:
                    if i['guest_name'] == guest_name and i['date_time'] == date_time:
                        the_party_bills.edit_party_bills(i, 'del')
                        break
            print('-------------------------------------------------------------')
            print('canceled')
            return
        else:
            print('-------------------------------------------------------------')
            print('enter 0 or 1')
            print('-------------------------------------------------------------')
    
def reserve_room():
    global rooms
    guest_name = input('guest\'s name: ')
    phone_number = input('phone number: ') # need function to check if the phone number is valid
    parties = json.load(open('parties.txt','r'))
    for i in range(len(parties)):
        if guest_name in parties[i]['members'] and phone_number == parties[i]['phone_number']:
            party_id = parties[i]['party_id']
            index = i
            break
    else:
        print('check guest info')
        return
    checkin_date, checkout_date, checkin_date_string, checkout_date_string = Inputs.check_in_out_date()
    n_single = int(input('how many single rooms the guest need: ')) # check the number <= 16
    n_double = int(input('how many double rooms the guest need: '))# check <= 16
    n_quadruple = int(input('how many quadruple rooms the guest need: ')) # check <= 4
    #single room available
    single_count = 0
    single_list = []
    for i in range(16):
        if rooms[i].check_room_schedule(checkin_date,checkout_date):
            single_count +=1
            single_list.append(i)
    #double room available
    double_count = 0
    double_list = []
    for i in range(16,32):
        if rooms[i].check_room_schedule(checkin_date,checkout_date):
            double_list.append(i)
            double_count +=1
    quadruple_count = 0
    quadruple_list  = []
    for i in range(32,36):
        if rooms[i].check_room_schedule(checkin_date,checkout_date):
            quadruple_list.append(i)
            quadruple_count +=1
    if single_count >= n_single and \
       double_count >= n_double and \
       quadruple_count >= n_quadruple:
        room_list = single_list[:n_single] + double_list[:n_double] + quadruple_list[:n_quadruple]
        parties[index]['rooms'] = room_list
        parties[index]['checkin_date'] = checkin_date_string
        parties[index]['checkout_date'] = checkout_date_string
        json.dump(parties,open('parties.txt','w'))
        print('reserve successfully!')
    else:
        print('room not available!')

    


def cancel_room():
    pass

################################################################################################
################################################################################################
################################################################################################
################################################################################################





    
