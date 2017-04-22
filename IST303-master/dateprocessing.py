from datetime import datetime, timedelta

class Datetimeperiod(object):
    def __init__(self, start_time, end_time, count):
        self.start_time = start_time
        self.end_time = end_time
        self.count = count

    def time_delta(self):
        return self.end_time - self.start_time

    def check_datetime_overlap(self, datetime):
        pass


def twoperiod(period1, period2):
    if period2.end_time <= period1.start_time:
        return [period1], [period2]
    elif period1.end_time > period2.end_time > period1.start_time and\
         period2.start_time < period1.start_time:
        return [Datetimeperiod(period1.start_time, period2.end_time, 2), \
                Datetimeperiod(period2.end_time, period1.end_time, 1)], \
               [Datetimeperiod(period2.start_time, period1.start_time, 1)]
    elif period2.end_time < period1.end_time and\
         period2.start_time > period1.start_time:
        period2.count += 1
        return [Datetimeperiod(period1.start_time, period2.start_time, 1), \
                period2, Datetimeperiod(period2.end_time, period1.end_time, 1)], \
               []
    elif period2.end_time > period1.end_time and\
         period2.start_time < period1.start_time:
        period1.count += 1
        return [period1], \
               [Datetimeperiod(period2.start_time, period1.start_time, 1), \
                Datetimeperiod(period1.end_time, period2.end_time, 1)]
    elif period1.end_time > period2.start_time > period1.start_time and\
         period2.end_time > period1.end_time:
        return [Datetimeperiod(period1.start_time, period2.start_time, 1), \
                Datetimeperiod(period2.start_time, period1.end_time, 2)], \
               [Datetimeperiod(period1.end_time, period2.end_time, 1)]
    elif period2.start_time >= period1.end_time:
        return [period1], [period2]
    elif period1.start_time == period2.start_time:
        if period2.end_time < period1.end_time:
            period2.count += 1
            return [period2, Datetimeperiod(period2.end_time, period1.end_time, 1)], []
        elif period2.end_time > period1.end_time:
            period1.count += 1
            return [period1], [Datetimeperiod(period1.end_time, period2.end_time, 1)]
        else:
            period1.count += 1
            return [period1], []
    elif period1.end_time == period2.end_time:
        if period2.start_time < period1.start_time:
            period1.count += 1
            return [period1], [Datetimeperiod(period2.start_time, period1.start_time, 1)]
        elif period2.start_time > period1.start_time:
            period2.count += 1
            return [Datetimeperiod(period1.start_time, period2.start_time, 1), period2], []
        else:
            period1.count += 1
            return [period1], []

def schedule_new(checked, unchecked):
    if len(unchecked) == 0:
        return []
    elif checked == []:
        checked.append(unchecked[0])
        return schedule_new(checked, unchecked[1:])
    else:
        period1 = checked[0]
        period2 = unchecked[0]
        checked_new, unchecked_new = twoperiod(period1, period2)
        return checked_new + schedule_new(checked[1:], unchecked_new + unchecked[1:])