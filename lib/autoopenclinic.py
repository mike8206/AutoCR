# customized functions
from lib.sys_func import readIdPwPin
from lib.web_driver_setting import web_driver_setting
from lib.login import login
from lib.clinic.clinic_open import clinic_open

def main(url_dict, vs_id_path, chrome_driver_path, ie_driver_path):
    # read portal credential from txt file
    vsidpw = {}
    vsidpw = readIdPwPin(vs_id_path)
    # chrome driver
    driver = web_driver_setting('chrome', chrome_driver_path, 'max')
    # login using chrome and get the session id
    session_id = login(driver, url_dict, vsidpw)
    driver.close()
    try:
        # IE driver
        driver_ie = web_driver_setting('ie', ie_driver_path, '')
        # open IE for open clinic
        clinic_open(driver_ie, url_dict, session_id)
        driver_ie.close()
    except Exception as error:
        driver_ie.close()
        raise ValueError('自動開診設定錯誤!! %s' % error)
