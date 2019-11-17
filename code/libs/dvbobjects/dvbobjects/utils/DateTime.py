import datetime

def get_date():
    '''This function return data 
    for TDT table'''

    date = datetime.datetime.now()
    now_date = int(date.year) - 1900
    now_month = int(date.strftime("%m"))
    now_day = int(date.strftime("%d"))
    now_hour_hex = int(date.strftime("%H"))
    now_min_hex = int(date.strftime("%M"))
    now_sec_hex = int(date.strftime("%S"))

    return (now_date, now_month, now_day, now_hour_hex, now_min_hex, now_sec_hex)