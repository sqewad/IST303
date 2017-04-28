from datetime import *
from Services import *

schedule =  [
                {
                    "end_time": "05/06/2017 20:00",
                    "guest_id": "0",
                    "guest_name": "a",
                    "start_time": "05/06/2017 19:00",
                    "time_of_reserving": "04/26/2017 13:27"
                },
                {
                    "end_time": "05/06/2017 17:00",
                    "guest_id": "0",
                    "guest_name": "a",
                    "start_time": "05/06/2017 16:00",
                    "time_of_reserving": "04/26/2017 13:28"
                }
            ]

service = Services('massage_shiatsu',4, 3.0, [30, 60],schedule)

def test_check_schecule():
    assert service.check_service_schedule(datetime(2017,5,6,17),datetime(2017,5,6,18)) == True
    assert service.check_service_schedule(datetime(2017,5,6,16),datetime(2017,5,6,17)) == True
    assert service.check_service_schedule(datetime(2017,5,6,19),datetime(2017,5,6,20)) == True