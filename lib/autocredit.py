# customized functions
from lib.sys_func import readIdPwPin, readDigiList
from lib.sys_web import callWebDriver
from lib.login import login
from lib.credit.credit_layout import clinicQuery, chooseClinic
from lib.credit.clinic_credit import modifyClinicCredit

def main(config_dict, url_dict): 
    cridpw = readIdPwPin(config_dict['cr_id_path'])

    # login using cardless driver and get the session id
    driver_ac = callWebDriver(config_dict, 'max')
    session_id = login(driver_ac, url_dict, cridpw)

    # get clinic arguments
    clinic_arg = clinicQuery(driver_ac, url_dict, session_id)
    
    if clinic_arg:
        # read VS list from txt file and select credit clinic
        vsiddict = readDigiList(config_dict['vslist_path'])
        vscredclinic = chooseClinic(driver_ac, url_dict, session_id, clinic_arg, vsiddict)

        if vscredclinic:
            modifyClinicCredit(driver_ac, url_dict, session_id, vscredclinic)