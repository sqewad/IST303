from datetime import *
from Guests import *
schedule = [
                {
                    "end_time": "05/06/2017 20:00",
                    "service": "massage_shiatsu",
                    "start_time": "05/06/2017 19:00",
                    "time_of_reserving": "04/26/2017 13:27"
                },
                {
                    "end_time": "05/06/2017 17:00",
                    "service": "massage_shiatsu",
                    "start_time": "05/06/2017 16:00",
                    "time_of_reserving": "04/26/2017 13:28"
                },
                {
                    "end_time": "05/06/2017 15:00",
                    "service": "mineral_bath",
                    "start_time": "05/06/2017 14:00",
                    "time_of_reserving": "04/26/2017 13:28"
                }
            ]

guest = Guests('a','0','0',schedule)

def test_check_schecule():
    assert guest.check_guest_schedule(datetime(2017,5,6,17),datetime(2017,5,6,18)) == True
    assert guest.check_guest_schedule(datetime(2017,5,6,16,30),datetime(2017,5,6,17,30)) == False
    assert guest.check_guest_schedule(datetime(2017,5,6,18),datetime(2017,5,6,19)) == True
    assert guest.check_guest_schedule(datetime(2017,5,6,15),datetime(2017,5,6,16)) == True

def test_check_mineral_bath_schecule():
    assert guest.check_mineral_bath(datetime(2017,5,6,17),datetime(2017,5,6,18)) == True
    assert guest.check_mineral_bath(datetime(2017,5,6,16,30),datetime(2017,5,6,17,30)) == False
    assert guest.check_mineral_bath(datetime(2017,5,6,11),datetime(2017,5,6,12)) == True
    assert guest.check_mineral_bath(datetime(2017,5,6,11,30),datetime(2017,5,6,12,30)) == False