from datetime import *

def service():
    while True:
        print('-------------------------------------------------------------')
        print('please choose 1 service')
        print('0. mineral bath' + '\n'
              '1. massage' + '\n'
              '2. facial' + '\n'
              '3. specialty treatment')
        service = input('enter the number of the service: ')
        if service in ['0', '1', '2', '3']:
            break
        else:
            print('-------------------------------------------------------------')
            print('please enter a number from 0 ~ 3, try again!')
    if service == '0':
        return 'mineral_bath'
    elif service == '1':
        while True:
            print('-------------------------------------------------------------')
            print('please choose 1 kind of massage')
            print('0. swedish' + '\n'
                  '1. shiatsu' + '\n'
                  '2. deep tissue')
            massage = input('enter the number of the kind: ')
            if massage == '0':
                return 'massage_swedish'
            elif massage == '1':
                return 'massage_shiatsu'
            elif massage == '2':
                return 'massage_deep_tissue'
            else:
                print('-------------------------------------------------------------')
                print('please enter a number from 0 ~ 2, try again!')
    elif service == '2':
        while True:
            print('-------------------------------------------------------------')
            print('please choose 1 kind of facial')
            print('0. normal' + '\n'
                  '1. collagen')
            facial = input('enter the number of the kind: ')
            if facial == '0':
                return 'facial_normal'
            elif facial == '1':
                return 'facial_collagen'
            else:
                print('-------------------------------------------------------------')
                print('please enter a number from 0 ~ 1, try again!')
    elif service == '3':
        while True:
            print('-------------------------------------------------------------')
            print('please choose 1 kind of specialty treatment')
            print('0. hot stone' + '\n'
                  '1. sugar scrub' + '\n'
                  '2. herbal body wrap' + '\n'
                  '3. botanical mud wrap')
            specialty_treatment = input('enter the number of the kind: ')
            if specialty_treatment == '0':
                return 'specialty_treatment_hot_stone'
            elif specialty_treatment == '1':
                return 'specialty_treatment_sugar_scrub'
            elif specialty_treatment == '2':
                return 'pecialty_treatment_herbal_body_wrap'
            elif specialty_treatment == '3':
                return 'specialty_treatment_botanical_mud_wrap'
            else:
                print('-------------------------------------------------------------')
                print('please enter a number from 0 ~ 3, try again!')

def service_date_time():
    while True:
        date_time_string = input('service\'s date and time (MM/DD/YYYY HH:MM): ')
        try:
            start_time = datetime.strptime(date_time_string, "%m/%d/%Y %H:%M")
            break
        except ValueError:
            print('-------------------------------------------------------------')
            print('please check the datetime and try again!')
    return date_time_string, start_time

def check_in_out_date():
    today = date.today()
    today_datetime = datetime.combine(today, datetime.min.time())
    while True:
        checkin_date_string = input('checkin date (MM/DD/YYYY): ')
        try:
            checkin_date = datetime.strptime(checkin_date_string, "%m/%d/%Y")
            if checkin_date >= today_datetime:
                break
            else:
                print('-------------------------------------------------------------')
                print('enter a date later than today, try again')
                print('-------------------------------------------------------------')
        except ValueError:
            print('-------------------------------------------------------------')
            print('please check the date and try again!')
            print('-------------------------------------------------------------')
    while True:
        checkout_date_string = input('checkout date (MM/DD/YYYY): ')
        try:
            checkout_date = datetime.strptime(checkout_date_string, "%m/%d/%Y")
            if checkout_date > checkin_date:
                break
            else:
                print('-------------------------------------------------------------')
                print('check-out date must be later than check-in date, try again')
                print('-------------------------------------------------------------')
        except ValueError:
            print('-------------------------------------------------------------')
            print('please check the date and try again!')
            print('-------------------------------------------------------------')
    return checkin_date, checkout_date, checkin_date_string, checkout_date_string


def length_of_service(service, services):
    while True:
        try:
            length_of_service = int(input('how many minutes does the guest want ' + \
                                          str(services[service].choice_of_length) + ': '))
            if length_of_service in services[service].choice_of_length:
                break
            else:
                print('please chose from ' + str(services[service].choice_of_length) + ' !')
        except ValueError:
            print('please enter a number!')
    return length_of_service

def input_date():
    today = date.today()
    while True:
        date_string = input('what date (MM/DD/YYYY): ')
        try:
            the_date = datetime.strptime(date_string, "%m/%d/%Y").date()
            if the_date >= today:
                break
            else:
                print('-------------------------------------------------------------')
                print('enter a date later than today, try again')
                print('-------------------------------------------------------------')
        except ValueError:
            print('-------------------------------------------------------------')
            print('please check the date and try again!')
            print('-------------------------------------------------------------')
    return the_date

def cancel_confirm():
    print('still wanna cancel?')
    while True:
        confirm = input('0. dont\'t cancel' + '\n'
                        '1. cancel' + '\n'
                        'enter the number: ')
        if confirm == '0':
            print('-------------------------------------------------------------')
            print('no cancelation!')
            print('-------------------------------------------------------------')
            return False
        elif confirm not in '01':
            print('-------------------------------------------------------------')
            print('enter 0 or 1')
            print('-------------------------------------------------------------')
            continue
        elif confirm == '1':
            return True