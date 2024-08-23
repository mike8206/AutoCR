from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# customized functions
from lib.sys_web import waitPageLoad

def digisignBGSign(driver, url_dict, session_id, vs_id_pw):
    try:
        temp_wait = WebDriverWait(driver, 60)
        # IE goto digisign page for background signing
        driver.get(url_dict['digisign_background_url'] + session_id)
        waitPageLoad(driver) 

        # input the pin
        waitPageLoad(driver)
        digiback_pin_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['digiback_pin'])))
        digiback_pin_ele.send_keys(vs_id_pw['pin'])
        
        # click the signing button
        waitPageLoad(driver)
        digiback_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['digiback_btn'])))
        digiback_btn.click()
        
        # 如果有延遲簽章的對話框, 就選擇臨床業務繁忙, 按下確認
        try:
            DDL_reason = temp_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, url_dict['digiback_ddl_reason'])))
            if DDL_reason:
                try:
                    DDL_reason.click()
                    waitPageLoad(driver)
                    DDL_confirm = temp_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, url_dict['digiback_ddl_confirm'])))
                    DDL_confirm.click()
                    sleep(0.5)
                except TimeoutException: 
                    # WebDriverWait throws TimeoutException if it fails
                    raise ValueError('背景簽章選擇延遲簽章原因失敗!!')
        except:
            pass

        # pause for 10 minutes
        sleep(600)

    except Exception as error:
        raise ValueError('背景簽章設定錯誤!! %s' % error)
    
    finally:
        try:
            driver.quit()
        except:
            pass