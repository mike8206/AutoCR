# customized functions
from lib.sys_web import callWebDriver
from lib.login import login
from lib.clinic.clinic_verifying import clinicVerifying

def main(config_dict, url_dict, func_string, id_pw): 
    if func_string == '請假確認':
        args = {'url': url_dict['clinic_offduty_verify_url'], 
                'list_ele': url_dict['verify_offduty_list'], 
                'apply_btn': url_dict['verify_offduty_btn'], 
                'back_btn': url_dict['verify_offduty_back']}
    elif func_string == '異動確認':
        args = {'url': url_dict['clinic_mod_verify_url'], 
                'list_ele': url_dict['verify_modify_list'], 
                'apply_btn': url_dict['verify_modify_btn'], 
                'back_btn': url_dict['verify_modify_back']}
    elif func_string == '門診護長確認':
        args = {'url': url_dict['clinic_mod_staffverify_url'], 
                'list_ele': url_dict['verify_staff_list'], 
                'apply_btn': url_dict['verify_staff_btn'], 
                'back_btn': url_dict['verify_staff_back']}
    
    # login using webdriver and get the session id
    driver = callWebDriver(config_dict, 'max')
    session_id = login(driver, url_dict, id_pw)

    clinicVerifying(driver, session_id, args)