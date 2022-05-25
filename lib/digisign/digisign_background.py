from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# customized functions
from lib.wait_page_load import wait_page_load

def digisign_background(driver_ie, url_dict, session_id, vsidpw):
    # IE goto digisign page for background signing
    driver_ie.get(url_dict['digisign_background_url'] + session_id)
    wait_page_load(driver_ie) 

    # input the pin
    wait_page_load(driver_ie) 
    driver_ie.find_element(By.ID, url_dict['digiback_pin']).send_keys(vsidpw['pin'])
    
    # click the signing button
    wait_page_load(driver_ie) 
    driver_ie.find_element(By.ID, url_dict['digiback_btn']).click()
    
    # 如果有延遲簽章的對話框, 就選擇臨床業務繁忙, 按下確認
    try:
        DDL_reason = WebDriverWait(driver_ie, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, url_dict['digiback_ddl_reason']))) # wait for 3 seconds
        if DDL_reason:
            try:
                DDL_reason.click()
                sleep(0.5)
                DDL_confirm = WebDriverWait(driver_ie, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, url_dict['digiback_ddl_confirm'])))
                DDL_confirm.click()
                sleep(0.5)
            except TimeoutException: # WebDriverWait throws TimeoutException if it fails
                raise ValueError('背景簽章選擇延遲簽章原因失敗!!')
    except:
        pass