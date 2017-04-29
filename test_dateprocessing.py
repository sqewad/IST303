from dateprocessing import *
from datetime import datetime, timedelta

period1 = Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),1)
period2 = Datetimeperiod(datetime(2017,4,5,1),datetime(2017,4,5,20),1)
period3 = Datetimeperiod(datetime(2017,4,4,5),datetime(2017, 4,4,10),1)
period4 = Datetimeperiod(datetime(2017,4,4,15),datetime(2017, 4,5,5),1)
period5 = Datetimeperiod(datetime(2017,4,4,5),datetime(2017, 4,4,15),1)
period6 = Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,4,15),1)
period7 = Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,15),1)
period8 = Datetimeperiod(datetime(2017,4,4,15),datetime(2017, 4,5,1),1)
period9 = Datetimeperiod(datetime(2017,4,4,5),datetime(2017, 4,5,1),1)
period10 = Datetimeperiod(datetime(2017,4,4,15),datetime(2017, 4,4,20),1)
period11 = Datetimeperiod(datetime(2017,4,4,5),datetime(2017, 4,5,5),1)

checked1 = [Datetimeperiod(datetime(2017,4,4,1),datetime(2017, 4,4,10),1),Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),1)]
unchecked1 = [Datetimeperiod(datetime(2017,4,5,1),datetime(2017,4,5,20),1)]
checked2 = [Datetimeperiod(datetime(2017,4,4,1),datetime(2017, 4,4,10),1),Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),1)]
unchecked2 = [Datetimeperiod(datetime(2017,4,4,15),datetime(2017,4,5,5),1)]
checked3 = [Datetimeperiod(datetime(2017,4,4,1),datetime(2017, 4,4,10),1),Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),1)]
unchecked3 = [Datetimeperiod(datetime(2017,4,4,15),datetime(2017,4,4,20),1)]

def rep(a):
    l= []
    for i in a[0]:
        l += [i.start_time, i.end_time, i.count]
    for i in a[1]:
        l += [i.start_time, i.end_time, i.count]
    return l

def rep_schedule_new(a):
    l = []
    for i in a:
        l += [i.start_time, i.end_time, i.count]
    return l
        

def test_twoperiod():
    assert rep(twoperiod(Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),2),period1)) == [datetime(2017,4,4,10),datetime(2017,4,5,1),3]
    assert rep(twoperiod(Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),2),period2)) == [datetime(2017,4,4,10),datetime(2017,4,5,1),2,datetime(2017,4,5,1),datetime(2017,4,5,20),1]
    assert rep(twoperiod(Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),2),period3)) == [datetime(2017,4,4,10),datetime(2017,4,5,1),2,datetime(2017,4,4,5),datetime(2017,4,4,10),1]
    assert rep(twoperiod(Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),2),period4)) == [datetime(2017,4,4,10),datetime(2017,4,4,15),2,datetime(2017,4,4,15),datetime(2017, 4,5,1),3,datetime(2017, 4,5,1),datetime(2017, 4,5,5),1]
    assert rep(twoperiod(Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),2),period5)) == [datetime(2017,4,4,10),datetime(2017,4,4,15),3,datetime(2017,4,4,15),datetime(2017, 4,5,1),2,datetime(2017, 4,4,5),datetime(2017, 4,4,10),1]
    assert rep(twoperiod(Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),2),period6)) == [datetime(2017,4,4,10),datetime(2017,4,4,15),3,datetime(2017,4,4,15),datetime(2017, 4,5,1),2]
    assert rep(twoperiod(Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),2),period7)) == [datetime(2017,4,4,10),datetime(2017,4,5,1),3,datetime(2017,4,5,1),datetime(2017, 4,5,15),1]
    assert rep(twoperiod(Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),2),period8)) == [datetime(2017,4,4,10),datetime(2017,4,4,15),2,datetime(2017,4,4,15),datetime(2017, 4,5,1),3]
    assert rep(twoperiod(Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),2),period9)) == [datetime(2017,4,4,10),datetime(2017,4,5,1),3,datetime(2017,4,4,5),datetime(2017, 4,4,10),1]
    assert rep(twoperiod(Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),2),period10)) == [datetime(2017,4,4,10),datetime(2017, 4,4,15),2,datetime(2017,4,4,15),datetime(2017,4,4,20),3,datetime(2017,4,4,20),datetime(2017, 4,5,1),2]
    assert rep(twoperiod(Datetimeperiod(datetime(2017,4,4,10),datetime(2017, 4,5,1),2),period11)) == [datetime(2017,4,4,10),datetime(2017, 4,5,1),3,datetime(2017,4,4,5),datetime(2017,4,4,10),1,datetime(2017,4,5,1),datetime(2017, 4,5,5),1]

def test_schedule_new():
    assert rep_schedule_new(schedule_new(checked1,unchecked1)) == [datetime(2017,4,4,1),datetime(2017, 4,4,10),1,datetime(2017,4,4,10),datetime(2017, 4,5,1),1,datetime(2017,4,5,1),datetime(2017,4,5,20),1]
    assert rep_schedule_new(schedule_new(checked2,unchecked2)) == [datetime(2017,4,4,1),datetime(2017, 4,4,10),1,datetime(2017,4,4,10),datetime(2017, 4,4,15),1,datetime(2017,4,4,15),datetime(2017,4,5,1),2,datetime(2017,4,5,1),datetime(2017,4,5,5),1]
    assert rep_schedule_new(schedule_new(checked3,unchecked3)) == [datetime(2017,4,4,1),datetime(2017, 4,4,10),1,datetime(2017,4,4,10),datetime(2017, 4,4,15),1,datetime(2017,4,4,15),datetime(2017,4,4,20),2,datetime(2017,4,4,20),datetime(2017,4,5,1),1]
