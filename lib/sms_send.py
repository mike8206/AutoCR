from time import sleep
from lib.wait_page_load import wait_page_load
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def splitSmsString(SMSstring):
    # Split SMSstring
    SMS_list =[]
    if len(SMSstring) <= 65:
        SMS_list.append(SMSstring)
    else:
        while len(SMSstring) >=65 :
            SMS_list.append(SMSstring[:65])
            SMSstring = "(續上)"+SMSstring[65:]
        SMS_list.append(SMSstring)
    return SMS_list

def sms_send(driver, url_dict, session_id, phone_list, SMSstring):
    tempWait = WebDriverWait(driver, 30)
    # go to send sms page
    driver.get(url_dict['send_sms_url'] + session_id)
    wait_page_load(driver)
    # set phon list to txt element, and set SMS to normal send
    driver.find_element(By.ID, url_dict['sms_phone_ele']).send_keys(phone_list)
    driver.find_element(By.ID, url_dict['sms_type_btn']).click()
    # call split SMS function
    SMS_list = splitSmsString(SMSstring)
    
    for sms_string in SMS_list:
        # find msg and send element
        msg_input_ele = tempWait.until(EC.element_to_be_clickable((By.ID, url_dict['sms_msg_input'])))
        send_btn_ele = tempWait.until(EC.element_to_be_clickable((By.ID, url_dict['sms_send_btn'])))
        msg_input_ele.clear()
        msg_input_ele.send_keys(sms_string)
        send_btn_ele.click()
        try:
            tempWait.until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
        except:
            continue
        sleep(2)
        wait_page_load(driver)