from selenium import webdriver

# customized functions
from lib.sys_func import readIdPwPin
from lib.login import login
from lib.clinic_open import clinic_open

# options
TIMEOUT = 5
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')

ie_options = webdriver.IeOptions()
ie_options.ignore_zoom_level = True

def main(url_dict, vs_id_path, chrome_driver_path, ie_driver_path):
    # read portal credential from txt file
    vsidpw = {}
    vsidpw = readIdPwPin(vs_id_path)
    # chrome driver
    driver = webdriver.Chrome(chrome_driver_path, options = chrome_options)
    driver.implicitly_wait(TIMEOUT)
    # login using chrome and get the session id
    session_id = login(driver, url_dict, vsidpw)
    try:
        # IE driver
        driver_ie = webdriver.Ie(ie_driver_path, options = ie_options)
        driver_ie.implicitly_wait(TIMEOUT)
        # open IE for open clinic
        clinic_open(driver_ie, url_dict, session_id)
    except Exception as error:
        driver_ie.close()
        raise ValueError('自動開診設定錯誤!! %s' % error)
