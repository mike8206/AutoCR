from selenium import webdriver

# customized functions
from lib.sys_func import readIdPwPin
from lib.login import login
from lib.patient_query import clinic_patient_query
from lib.patient_query import exam_patient_query
from lib.phone_get import phone_get

# options
TIMEOUT = 5
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')

def main(url_dict, cr_id_path, origin_type, chrome_driver_path):
    # read portal credential from txt file
    cridpw = {}
    cridpw = readIdPwPin(cr_id_path)
    # chrome driver
    driver = webdriver.Chrome(chrome_driver_path, options = chrome_options)
    driver.implicitly_wait(TIMEOUT)
    # login using chrome and get the session id
    session_id = login(driver, url_dict, cridpw)
    try:
        # get patient list
        if origin_type == 'clinic':
            patientlist = clinic_patient_query(driver, url_dict, session_id)
        else:
            patientlist = exam_patient_query(driver, url_dict, session_id)
    except Exception as error:
        driver.close()
        raise ValueError('自動擷取病人病歷號設定錯誤!! %s' % error)
    try:
        # transfer pt list to get phone function
        phone_get(driver, url_dict, session_id, patientlist)
    except Exception as error:
        driver.close()
        raise ValueError('從櫃台作業查電話設定錯誤!! %s' % error)