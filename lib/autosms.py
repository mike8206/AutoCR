from selenium import webdriver

# customed functions
from lib.google_calendar import google_calendar
from lib.login import login
from lib.send_sms import send_sms

# options
TIMEOUT = 5
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')

def main(url_dict, cr_id_path, phone_path, google_secret_path, google_token_path, google_cal_id, chrome_driver_path):
    # read portal credential from txt file
    cridpw = {}
    try:
        with open(cr_id_path, encoding="UTF-8") as f:
            idpwpin = f.read().splitlines()
            # id pw (帳號 密碼)
            cridpw['id']=idpwpin[0]
            cridpw['pw']=idpwpin[1]
    except:
        raise ValueError('CR帳號密碼檔案錯誤!!')

    try:
        with open(phone_path, encoding="UTF-8") as f:
            phone_list = f.read()
    except:
        raise ValueError('簡訊檔案錯誤!!')

    if len(google_cal_id) != 0:
        # get event from google calendar
        SMSstring = google_calendar(google_secret_path, google_token_path, google_cal_id)
        # chrome driver
        driver = webdriver.Chrome(chrome_driver_path, options = chrome_options)
        driver.implicitly_wait(TIMEOUT)
        # login using chrome and get the session id
        session_id = login(driver, url_dict, cridpw)
        # send sms
        send_sms(driver, url_dict, session_id, phone_list, SMSstring)
    else:
        raise ValueError('未設定Google日曆ID!!')
