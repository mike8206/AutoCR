# customized functions
from lib.sys_func import readIdPwPin
from lib.web_driver_setting import web_driver_setting
from lib.login import login
from lib.clinic.clinic_query import clinic_query
from lib.clinic.clinic_credit import clinic_credit

def main(url_dict, cr_id_path, chrome_driver_path):
    # read portal credential from txt file
    cridpw = {}
    try:
        cridpw = readIdPwPin(cr_id_path)
    except:
        raise ValueError('CR帳號密碼檔案錯誤!!')
    # login using chrome and get the session id
    driver = web_driver_setting('chrome', chrome_driver_path, 'max')
    session_id = login(driver, url_dict, cridpw)
    try:
        # get clinic args
        vscredclinic = clinic_query(driver, url_dict, session_id)
    except Exception as error:
        driver.close()
        raise ValueError('查詢診間設定錯誤!! %s' % error)
    try:
        # open credit function
        clinic_credit(driver, url_dict, session_id, vscredclinic)
        driver.close()
    except Exception as error:
        driver.close()
        raise ValueError('改績效設定錯誤!! %s' % error)