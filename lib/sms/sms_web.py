from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

# customized functions
from lib.sys_web import waitPageLoad

def smsSend(driver, url_dict, session_id, sendtype, phone_list, SMS_list):
    try:
        temp_wait = WebDriverWait(driver, 30)

        # Navigate to the send SMS page
        driver.get(url_dict['send_sms_url'] + session_id)
        waitPageLoad(driver)

        # Set the phone list or ID based on the sendtype
        if sendtype == "phone":
            sms_phone_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['sms_phone_ele'])))
            sms_phone_ele.send_keys(phone_list)
        elif sendtype == "id":
            sms_id_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['sms_id_ele'])))
            sms_id_ele.send_keys(phone_list)
        
        # Set SMS sending type to normal
        sms_type_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['sms_type_btn'])))
        sms_type_btn.click()
        
        # Send SMS messages from the list
        for sms_string in SMS_list:
            msg_input_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['sms_msg_input'])))
            send_btn_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['sms_send_btn'])))
            
            # Clear the input and send the SMS message 
            msg_input_ele.clear()
            msg_input_ele.send_keys(sms_string)
            send_btn_ele.click()
            
            # Handle alert if present, otherwise continue
            try:
                temp_wait.until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
            except TimeoutException:
                continue

            sleep(5)
            waitPageLoad(driver)

    except Exception as error:
        raise ValueError('寄送簡訊失敗!! %s' % error)
    
    finally:
        try:
            driver.quit()
        except:
            pass