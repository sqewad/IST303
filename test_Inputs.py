from Inputs import *
from datetime import *
import mock
import project

def test_cancel_confirm():
    with mock.patch('builtins.input', side_effect=['0', 'a', '1', 'a', '0']):
        assert cancel_confirm() is False
        assert cancel_confirm() == True
        assert cancel_confirm() is False

def test_input_date():
    with mock.patch('builtins.input', side_effect=['0', '05/05/2300', '01/01/2016', '06/06/2300']):
        assert input_date() == date(2300,5,5)
        assert input_date() == date(2300,6,6)

def test_length_of_service():
    with mock.patch('builtins.input', side_effect=['0', '60', 'a', '90']):
        assert length_of_service('mineral_bath',project.services) == 60
        assert length_of_service('mineral_bath',project.services) == 90

def test_check_in_out_date():
    with mock.patch('builtins.input', side_effect=['a', '01/01/2016', '05/05/2300', '01/01/2016', '06/06/2300']):
        assert check_in_out_date() == (datetime(2300, 5, 5), datetime(2300, 6, 6), '05/05/2300', '06/06/2300')

def test_service_date_time():
    with mock.patch('builtins.input', side_effect=['a', '01/01/2016 25:00', '05/05/2300 18:00', '01/41/2016', '06/06/2300 5:00']):
        assert service_date_time() == ('05/05/2300 18:00', datetime(2300, 5, 5, 18))
        assert service_date_time() == ('06/06/2300 5:00', datetime(2300, 6, 6, 5))

def test_service():
    with mock.patch('builtins.input', side_effect=['a', '0','1', '3', '2', '2', 'b', '1', '3', '4', '3']):
        assert service() == 'mineral_bath'
        assert service() == 'massage_deep_tissue'
        assert service() == 'facial_collagen'
        assert service() == 'specialty_treatment_botanical_mud_wrap'