# customized functions
from lib.sys_func import readIdPwPin
from lib.web_driver_setting import web_driver_setting
from lib.login import login
from lib.sms.google_calendar import google_calendar
from lib.sms.sms_send import sms_send

def main(url_dict, cr_id_path, phone_path, google_secret_path, google_token_path, google_cal_id, chrome_driver_path):
    # read portal credential from txt file
    cridpw = {}
    cridpw = readIdPwPin(cr_id_path)
    try:
        with open(phone_path, encoding="UTF-8") as f:
            phone_list = f.read()
    except:
        raise ValueError('簡訊清單檔案錯誤!!')
    if len(google_cal_id) != 0:
        # get event from google calendar
        SMSstring = google_calendar(google_secret_path, google_token_path, google_cal_id)
        # chrome driver
        driver = web_driver_setting('chrome', chrome_driver_path, 'max')
    else:
        raise ValueError('未設定Google日曆ID!!')
    # login using chrome and get the session id
    session_id = login(driver, url_dict, cridpw)
    try:
        # send sms
        sms_send(driver, url_dict, session_id, phone_list, SMSstring)
        driver.close()
    except Exception as error:
        driver.close()
        raise ValueError('寄送簡訊失敗!! %s' % error)