from Rooms import *
from datetime import datetime,timedelta
import json

def get_info_for_shorten_stay():
    now = datetime.now()
    guests = json.load(open('guests.txt', 'r'))
    parties = json.load(open('parties.txt', 'r'))
    while 1:
        guest_name = input('guest\'s name: ')
        room_number = input('room number: ')
        for i in parties:
            if guest_name in i['members'] and room_number in i['rooms'] and i['status'] == 'checkin':
                party_id = i['party_id']
                checkin_date_str = i['checkin_date']
                checkout_date_str = i['checkout_date']
                checkout_date = datetime.strptime(checkout_date_str, "%m/%d/%Y")
                checkin_date = datetime.strptime(checkin_date_str, "%m/%d/%Y")
                diff = checkout_date - checkin_date
                roomsnum = i['rooms']
                index = parties.index(i)
                break
        else:
            print('-------------------------------------------------------------')
            print('check information, try again')
            print('-------------------------------------------------------------')
            continue
        break
    while True:
        try:
            days = int(input('days you want cancel: '))
            if 1 <= days <= diff.days-1:
                break
            else:
                print('-------------------------------------------------------------')
                print('you can shorten at least one day, ' + str(diff.days-1) + ' at most. try again!')
                print('-------------------------------------------------------------')
        except:
            print('-------------------------------------------------------------')
            print('please enter a number!')
            print('-------------------------------------------------------------')
    cancel_date_str_list = []
    for i in range(diff.days-days, diff.days+1):
        cancel_date = checkin_date + timedelta(i)
        cancel_date_str = cancel_date.strftime('%m/%d/%Y')
        cancel_date_str_list.append(cancel_date_str)
    return guests, parties, party_id, checkin_date, checkout_date, roomsnum, index, days, cancel_date_str_list


def changeReservation(rooms, guests, parties, party_id, checkin_date, checkout_date, roomsnum, index, days, cancel_date_str_list):
    """  Guests who check-in for at least one night may shorten the length of their reservation; 
         a 75% refund is given for days dropped to make the reservation shorter.
    """
    # Assumption: if customer wanna to stay longer than what they reseved before

    # [int(i) for i in checkin_date_str.split('/')]
    diff = checkout_date - checkin_date
    refund = 0.75
    if days == 0:
        return
    elif 1 <= days <= diff.days-1:
        # print('You are available to manage your resevation.')
        new_checkout_date = checkout_date - timedelta(days)
        new_checkout_date_str = new_checkout_date.strftime('%m/%d/%Y')
        parties[index]['checkout_date'] = new_checkout_date_str

        party_bills = json.load(open('parties_bills/' + party_id + '.txt', 'r'))

        # numRooms = len(parties[index]['rooms'])
        for i in range(len(party_bills)):
            if party_bills[i]['date_time'] in cancel_date_str_list:
                party_bills[i]['item'] += ' (canceled)'
                party_bills[i]['charge'] *= 1-refund

        for i in roomsnum:
            room_schedules = rooms[int(i)].schedule
            # room_schedules = json.load(open('rooms_schedules/' + i +'.txt', 'r'))
            for j in range(len(room_schedules)):
                if room_schedules[j]['party_id'] == party_id:
                    room_schedules[j]['checkout_date'] = new_checkout_date_str
            json.dump(room_schedules, open('rooms_schedules/' + i + '.txt', 'w'), sort_keys=True, indent=4)
        json.dump(party_bills, open('parties_bills/' + party_id + '.txt', 'w'), sort_keys=True, indent=4)
        json.dump(parties, open('parties.txt', 'w'), sort_keys=True, indent=4)
        print('successfully re-schedule room')
        print('-------------------------------------------------------------')
    else:
        pass
        # re enter days, need another loop




    ##  Assumption: We can assume that if customer want to resechedule room resevation, 
    ### they have to cancale room until the last day of previous resevation.







