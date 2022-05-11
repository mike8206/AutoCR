from datetime import datetime, timedelta
from os.path import exists
from pytz import timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# SCOPES
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/calendar.events.readonly']

# AMPM
taiwan_taipei = timezone('Asia/Taipei')
today = datetime.now(taiwan_taipei)
nowhour = today.strftime("%H")

if int(nowhour) < 12:
    am = True

def start_end_time():
    if am == True:
        tomorrow = today + timedelta(days=1)
        starttime = (datetime(today.year, today.month, today.day, today.hour, today.minute)).isoformat() + 'Z'
        endtime =  (datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00)).isoformat() + 'Z'
    else:
        weekday = today.weekday()
        if weekday >= 5:
            if weekday == 5:
                monday = today + timedelta(days=3)       
            elif weekday == 6:
                monday = today + timedelta(days=2)
            else:
                monday = today + timedelta(days=1)
            tomorrow = monday + timedelta(days=1) 
            starttime = (datetime(monday.year, monday.month, monday.day, 00, 00)).isoformat() + 'Z'
            endtime =  (datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00)).isoformat() + 'Z'
        else:
            tomorrow = today + timedelta(days=1)
            dayaftertomorrow = today + timedelta(days=2)
            starttime = (datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00)).isoformat() + 'Z'
            endtime =  (datetime(dayaftertomorrow.year, dayaftertomorrow.month, dayaftertomorrow.day, 00, 00)).isoformat() + 'Z'
    startendtime = [starttime, endtime]
    return startendtime

def date_week_string(starttime):
    date = datetime.strptime(starttime, "%Y-%m-%dT%H:%M:%S%z")
    weekstring = week_day(date)
    datestring = date.strftime('%m/%d')
    dateweekstring = datestring+weekstring
    return dateweekstring
    
def week_day(date):
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

def SMS_string(events, starttime):
    if not events:
        eventstring = ''
    else:
        eventstring = ''
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            event_time = event_start.strftime('%H:%M')
            eventstring = eventstring + event_time + " " + event['summary']+"；"
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
            SMSstring = "各位同仁辛苦了，請記得電子簽章，"+date_week_string(starttime)+eventstring
    return SMSstring

def google_calendar(google_secret_path, google_token_path):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if exists(google_token_path):
        creds = Credentials.from_authorized_user_file(google_token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                google_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(google_token_path, 'w') as token:
            token.write(creds.to_json())
    
    startendtime = start_end_time()

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        events_result = service.events().list(calendarId='primary', timeMin=startendtime[0], timeMax = startendtime[1],
                                              singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        SMSstring = SMS_string(events, startendtime[0])
        return SMSstring
    
    except HttpError as error:
        raise ValueError('An error occurred: %s' % error)