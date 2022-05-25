from datetime import datetime, timedelta
from os.path import exists
from pytz import timezone, utc

# from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# SCOPES
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/calendar.events.readonly']

def startEndTime(am, today, timeZone):
    if am == True:
        tomorrow = today + timedelta(days=1)
        starttime = datetime(today.year, today.month, today.day, today.hour, today.minute).astimezone(timeZone)
        endtime =  datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00).astimezone(timeZone)
    else:
        weekday = today.weekday()
        if weekday >= 4:
            if weekday == 4:
                monday = today + timedelta(days=3)       
            elif weekday == 5:
                monday = today + timedelta(days=2)
            else:
                monday = today + timedelta(days=1)
            tomorrow = monday + timedelta(days=1) 
            starttime = datetime(monday.year, monday.month, monday.day, 00, 00).astimezone(timeZone)
            endtime =  datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00).astimezone(timeZone)
        else:
            tomorrow = today + timedelta(days=1)
            dayaftertomorrow = today + timedelta(days=2)
            starttime = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00).astimezone(timeZone)
            endtime =  datetime(dayaftertomorrow.year, dayaftertomorrow.month, dayaftertomorrow.day, 00, 00).astimezone(timeZone)
    start_end_time = [starttime.astimezone(utc).isoformat().split('+')[0]+'Z', endtime.astimezone(utc).isoformat().split('+')[0]+'Z']
    return start_end_time

def dateWeekToString(starttime, timeZone):
    # starttime in UTC
    date = datetime.strptime(starttime, "%Y-%m-%dT%H:%M:%S%z").astimezone(timeZone)
    weekstring = weekdayToString(date)
    datestring = date.strftime('%m/%d')
    dateweekstring = datestring+weekstring
    return dateweekstring
    
def weekdayToString(date):
    weekday = date.weekday()
    if weekday == 0:
        weekstring = "（一）"
    elif weekday == 1:
        weekstring = "（二）"
    elif weekday == 2:
        weekstring = "（三）"
    elif weekday == 3:
        weekstring = "（四）"
    elif weekday == 4:
        weekstring = "（五）"
    else:
        weekstring = ""
    return weekstring

def eventToSmsString(events, starttime, timeZone, am):
    eventlist = []
    eventstring = ''
    if not events:
        pass
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            event_time = event_start.strftime('%H:%M')
            eventname = event_time + " " + event['summary']
            eventlist.append(eventname)
        eventlist.sort()
        for item in eventlist:
            eventstring = eventstring+item+"；"
        eventstring = eventstring.removesuffix('；')
    
    if am == True:
        if eventstring == '':
            SMSstring = "各位同仁早！今日無其他行程。"
        else:
            SMSstring = "各位同仁早！今日 " + eventstring
    else:
        if eventstring == '':
            SMSstring = "各位同仁辛苦了，請記得電子簽章。"
        else:
            SMSstring = "各位同仁辛苦了，請記得電子簽章，"+dateWeekToString(starttime, timeZone)+eventstring
    return SMSstring

def google_calendar(google_secret_path, google_token_path, google_cal_id):
    # AMPM
    timeZone = timezone('Asia/Taipei')
    today = datetime.now(timeZone)
    nowhour = today.strftime("%H")
    am = False

    if int(nowhour) < 12:
        am = True

    creds = None
    if exists(google_token_path):
        creds = Credentials.from_authorized_user_file(google_token_path, SCOPES)
    if not creds or not creds.valid:
        # if creds and creds.expired and creds.refresh_token:
            # creds.refresh(Request())
        # else:
        flow = InstalledAppFlow.from_client_secrets_file(
                google_secret_path, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(google_token_path, 'w') as token:
            token.write(creds.to_json())
    
    start_end_time = startEndTime(am, today, timeZone)

    try:
        service = build('calendar', 'v3', credentials=creds)
        event_list = []
        # Call the Calendar API
        for calendar in google_cal_id:
            try:
                calendar_result = service.events().list(calendarId=calendar, timeMin=start_end_time[0], timeMax = start_end_time[1],
                                                    singleEvents=True, orderBy='startTime').execute()
                events = calendar_result.get('items', [])
                event_list.extend(events)
            except:
                continue
        SMSstring = eventToSmsString(event_list, start_end_time[0], timeZone, am)
        return SMSstring
    
    except HttpError as error:
        raise ValueError('An error occurred: %s' % error)
