from pytz import timezone, utc
from datetime import datetime, timedelta

# customized functions
from lib.sys_func import currentDateTime

TIMEZONE = timezone('Asia/Taipei')

def startEndTime():
    date_arg = currentDateTime()
    date_1 = date_arg['now']
    weekday = date_arg['weekday']
    start_time = None
    
    if int(date_arg['hour']) < 12:
        start_time = datetime(date_1.year, date_1.month, date_1.day, date_1.hour, date_1.minute).astimezone(TIMEZONE)
    else:
        offset = 3 if weekday == 4 else 2 if weekday == 5 else 1
        date_1 = date_1 + timedelta(days=offset)
        start_time = datetime(date_1.year, date_1.month, date_1.day, 00, 00).astimezone(TIMEZONE)
    date_2 = date_1 + timedelta(days=1)
    end_time =  datetime(date_2.year, date_2.month, date_2.day, 00, 00).astimezone(TIMEZONE)
    start_end_time = [start_time.astimezone(utc).isoformat().split('+', 1)[0]+'Z', 
                      end_time.astimezone(utc).isoformat().split('+', 1)[0]+'Z']
    return start_end_time

def eventListToString(gg_event_list, sms_text_dict):
    event_string = ''
    if len(gg_event_list):
        event_list = []
        for event in gg_event_list:
            start_date_time = event['start'].get('dateTime', event['start'].get('date'))
            try:
                event_start = datetime.strptime(start_date_time, "%Y-%m-%dT%H:%M:%S%z")
                event_time = event_start.strftime('%H:%M')
            except ValueError:
                event_time = sms_text_dict['allday']
            event_name = event_time + " " + event['summary']
            event_list.append(event_name)
        event_list = list(dict.fromkeys(event_list))
        event_list.sort()
        for item in event_list:
            event_string = event_string+item+"；"
        event_string = event_string.removesuffix('；')
    return event_string

def dateToString(date_time):
    date_string = date_time.strftime('%m/%d')
    return date_string

def weekdayToString(date_time, sms_text_dict):
    weekday = date_time.weekday()
    weekday_map = {
        0: 'Mon',
        1: 'Tue',
        2: 'Wed',
        3: 'Thu',
        4: 'Fri',
        5: 'Sat',
        6: 'Sun',
    }
    # Retrieve the corresponding string from the dictionary
    return sms_text_dict.get(weekday_map.get(weekday, ''), '')  # Default to empty string if key not found

def eventToSmsString(start_end_time, sms_text_dict, event_string):
    # start_time in UTC
    date_time = datetime.strptime(start_end_time[0], "%Y-%m-%dT%H:%M:%S%z").astimezone(TIMEZONE)
    date_string = dateToString(date_time)
    weekstring = weekdayToString(date_time, sms_text_dict)
    date_arg = currentDateTime()
    if int(date_arg['hour']) < 12:
        if event_string == '':
            event_string = sms_text_dict['noevent']
        SMSstring = sms_text_dict['amtext_prefix'] + event_string
    else:
        if event_string == '':
            SMSstring = sms_text_dict["pmtext_prefix"]+sms_text_dict["end"]
        else:
            if date_arg['weekday'] < 4:
                smsprefix = sms_text_dict["pmtext_prefix"]
            else:
                smsprefix = sms_text_dict["fripmtext_prefix"]
            SMSstring = smsprefix+sms_text_dict["comma"]+date_string+weekstring+event_string
    return SMSstring

def splitSmsString(SMSstring):
    # Split SMSstring
    SMS_list =[]
    if len(SMSstring) <= 65:
        SMS_list.append(SMSstring)
    else:
        while len(SMSstring) >65 :
            SMS_list.append(SMSstring[:65])
            SMSstring = "(續上)"+SMSstring[65:]
        SMS_list.append(SMSstring)
    return SMS_list