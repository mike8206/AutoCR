from selenium import webdriver

# customized functions
from lib.login import login
from lib.clinic_query import clinic_query
from lib.clinic_credit import clinic_credit

# options
TIMEOUT = 5
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')

def main(url_dict, cr_id_path, chrome_driver_path):
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
    # chrome driver
    driver = webdriver.Chrome(chrome_driver_path, options = chrome_options)
    driver.implicitly_wait(TIMEOUT)
    # login using chrome and get the session id
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
    except Exception as error:
        driver.close()
        raise ValueError('改績效設定錯誤!! %s' % error)
    