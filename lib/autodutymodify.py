from selenium import webdriver

# customized functions

from lib.login import login
from lib.clinic_verifying import clinic_verifying

# options
TIMEOUT = 5
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')

def main(url_dict, funcstring, data, chrome_driver_path): 
    if funcstring == '請假確認':
        args = {'url': url_dict['clinic_offduty_verify_url'], 'list_ele': url_dict['verify_offduty_list'], 'apply_btn': url_dict['verify_offduty_btn'], 'back_btn': url_dict['verify_offduty_back']}
    elif funcstring == '異動確認':
        args = {'url': url_dict['clinic_mod_verify_url'], 'list_ele': url_dict['verify_modify_list'], 'apply_btn': url_dict['verify_modify_btn'], 'back_btn': url_dict['verify_modify_back']}
    elif funcstring == '門診護長確認':
        args = {'url': url_dict['clinic_mod_staffverify_url'], 'list_ele': url_dict['verify_staff_list'], 'apply_btn': url_dict['verify_staff_btn'], 'back_btn': url_dict['verify_staff_back']}
    
    # chrome driver
    driver = webdriver.Chrome(chrome_driver_path, options = chrome_options)
    driver.implicitly_wait(TIMEOUT)
    # login using chrome and get the session id
    session_id = login(driver, url_dict, data)

    try:
        # '請假確認','異動確認','門診護長確認'
        clinic_verifying(driver, session_id, args)
        driver.close()
    except Exception as error:
        driver.close()
        raise ValueError('自動請假異動設定錯誤!! %s' % error)
