from threading import Thread

# customized functions
from lib.sys_func import readIdPwPin, readDigiList, readSMStext
from lib.sys_web import callWebDriver
from lib.login import login
from lib.digisign.digisign_count import countDigisignNum
from lib.digisign.digisign_transfer import transferDigisign
from lib.digisign.digisign_background import digisignBGSign
from lib.digisign.digisign_query import digisignQuerySign
from lib.sms.sms_func import splitSmsString
from lib.sms.sms_web import smsSend

def main(config_dict, url_dict):
    # read portal credential from txt file
    vs_id_pw = readIdPwPin(config_dict['vs_id_path'])
    cr_id_pw = readIdPwPin(config_dict['cr_id_path'])

    # read doctor list from txt file (for digital signature)
    doctor_list = readDigiList(config_dict['list_path'])
    
    # read SMS sentences
    sms_text_dict = readSMStext(config_dict['sms_path'])

    # use webdriver for login
    driver = callWebDriver(config_dict, 'max')
    session_id = login(driver, url_dict, vs_id_pw)

    # use webdriver for check left amount
    left_digi = countDigisignNum(driver, url_dict, session_id)
    backgroundsign = False

    if left_digi > 100:
        # send alert message to CR
        SMS_string = sms_text_dict['left_digi_prefix']+str(left_digi)+sms_text_dict['left_digi_suffix']+sms_text_dict['left_digi_warning']
        SMS_list = splitSmsString(SMS_string)
        driver2 = callWebDriver(config_dict, 'headless')
        smsSend(driver2, url_dict, session_id, "id", cr_id_pw['id'], SMS_list)

        # open webdriver for background signing
        driver3 = callWebDriver(config_dict, 'max')
        backgroundsign = True
        Thread(target=digisignBGSign, args=[driver3, url_dict, session_id, vs_id_pw], daemon=True).start()

    # use webdriver for digisign replacing all IDs
    unsignlist = transferDigisign(driver, url_dict, session_id, vs_id_pw, doctor_list)
    
    if not backgroundsign:
        # DSquery signing
        driver3 = callWebDriver(config_dict, 'max')
        digisignQuerySign(config_dict, driver3, url_dict, session_id, vs_id_pw)
    
    # send SMS to notice unsign ppl
    if unsignlist:
        id_list = ",".join(unsignlist)
        
        SMS_string = sms_text_dict['digi_reminder']+sms_text_dict['left_digi_warning']
        SMS_list = splitSmsString(SMS_string)
        
        driver2 = callWebDriver(config_dict, 'headless')
        session_id = login(driver2, url_dict, cr_id_pw)
        smsSend(driver2, url_dict, session_id, "id", id_list, SMS_list)