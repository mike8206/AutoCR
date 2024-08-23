from os.path import exists
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from lib.timeout import timeOut

# SCOPES
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/calendar.events.readonly']

@timeOut(30)
def googleRefreshToken(google_secret_path, google_token_path):
    flow = InstalledAppFlow.from_client_secrets_file(
                google_secret_path, SCOPES)
    creds = flow.run_local_server(port=0)
    if creds:
        with open(google_token_path, 'w') as token:
            token.write(creds.to_json())
    return creds

def googleCred(google_secret_path, google_token_path):
    creds = None
    if exists(google_token_path):
        creds = Credentials.from_authorized_user_file(google_token_path, SCOPES)

    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                creds = googleRefreshToken(google_secret_path, google_token_path)
        except:
            creds = googleRefreshToken(google_secret_path, google_token_path)
    return creds

def googleCalendar(config_dict, start_end_time):
    google_secret_path = config_dict['google_secret_path']
    google_token_path = config_dict['google_token_path']
    google_cal_id = config_dict['google_cal_id']
    creds = googleCred(google_secret_path, google_token_path)
    event_list = []
    try:
        service = build('calendar', 'v3', credentials=creds, static_discovery=False)
        # Call the Calendar API
        for calendar in google_cal_id:
            try:
                calendar_result = service.events().list(calendarId=calendar, timeMin=start_end_time[0], timeMax=start_end_time[1],
                                                    singleEvents=True, orderBy='startTime').execute()
                events = calendar_result.get('items', [])
                event_list.extend(events)
            except:
                continue
        return event_list
    except HttpError as error:
        raise ValueError('An error occurred: %s' % error)