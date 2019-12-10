from datetime import *
from dateutil.rrule import *
from dateutil.parser import *
import time


def get_datetime():
    '''This function retrun current and
    change time for TDT and TOT tables'''

    current_time = time.gmtime()
    current_local_time = time.localtime()

    # italian rules
    current_offset_polarity = 0x0 # positive
    if current_local_time.tm_isdst == 1:
        start = 'DTSTART:%(year)04d%(month)02d%(day)02dT%(hour)02d%(minute)02d%(second)02d\n' % { 
            "year": current_time[0], 
            "month": current_time[1], 
            "day": current_time[1], 
            "hour" : 3, 
            "minute": 0, 
            "second": 0
        }
        start += 'RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10;COUNT=1' # last sunday of october
        current_offset = 0x02
        new_offset = 0x01
    else:
        start = 'DTSTART:%(year)04d%(month)02d%(day)02dT%(hour)02d%(minute)02d%(second)02d\n' % { 
            "year": current_time[0], 
            "month": current_time[1], 
            "day": current_time[1], 
            "hour" : 2, 
            "minute": 0, 
            "second": 0
        }
        start += 'RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=3;COUNT=1' # last sunday of march
        current_offset = 0x01
        new_offset = 0x02

    change_time = list(rrulestr(start))[0]

    return (current_time, change_time, new_offset)
