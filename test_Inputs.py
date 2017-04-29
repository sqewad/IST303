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
