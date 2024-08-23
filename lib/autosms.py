# customized functions
from lib.sys_func import readIdPwPin, readGSM, readSMStext
from lib.sys_web import callWebDriver
from lib.login import login
from lib.sms.google_calendar import googleCalendar
from lib.sms.sms_func import startEndTime, eventListToString, eventToSmsString, splitSmsString
from lib.sms.sms_web import smsSend

def main(config_dict, url_dict):
    # read portal credential from txt file
    cr_id_pw = readIdPwPin(config_dict['cr_id_path'])

    # read GSM list
    gsm_list = readGSM(config_dict['phone_path'])

    # read SMS sentences
    sms_text_dict = readSMStext(config_dict['sms_path'])
    
    if len(config_dict['google_cal_id']) != 0:
        # get event from google calendar
        start_end_time = startEndTime()
        event_list = googleCalendar(config_dict, start_end_time)
        event_string = eventListToString(event_list, sms_text_dict)
        SMS_string = eventToSmsString(start_end_time, sms_text_dict, event_string)

        # call split SMS function
        SMS_list = splitSmsString(SMS_string)
    else:
        raise ValueError('未設定Google日曆ID!!')

    # use webdriver for login
    driver = callWebDriver(config_dict, 'max')
    session_id = login(driver, url_dict, cr_id_pw)
    
    # send sms
    smsSend(driver, url_dict, session_id, "phone", gsm_list, SMS_list)