# customized functions
from lib.sys_func import readIdPwPin
from lib.sys_web import callWebDriver
from lib.login import login
from lib.clinic.clinic_open import clinicOpen

def main(config_dict, url_dict):
    # read portal credential from txt file
    vs_id_pw = readIdPwPin(config_dict['vs_id_path'])

    # use driver for login    
    driver = callWebDriver(config_dict, 'max')
    session_id = login(driver, url_dict, vs_id_pw)
    
    clinicOpen(driver, url_dict, session_id, config_dict, vs_id_pw)