from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# customized functions
from lib.sys_web import waitPageLoad
from lib.sys_func import checkIfProcessRunning

def digisignQuerySign(config_dict, driver, url_dict, session_id, vs_id_pw):
    try:
        temp_wait = WebDriverWait(driver, 300)

        # IE goto digisign page for background signing
        driver.get(url_dict['digisign_query_url'] + session_id)
        waitPageLoad(driver) 

        looptime = 0
        now_digi_num = ''
        while now_digi_num != '0筆' and looptime < 10:
            # check remaining
            refresh_btn_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['digiquery_refresh_btn'])))
            refresh_btn_ele.click()
            waitPageLoad(driver)

            show_of_digisign = temp_wait.until(EC.text_to_be_present_in_element((By.ID, url_dict['digiquery_count_text']), '筆'))
            if show_of_digisign:
                num_of_digisign = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['digiquery_count_text'])))
                now_digi_num = num_of_digisign.text
                if looptime > 1 and last_digi_num == now_digi_num:
                    raise ValueError('兩次剩餘筆數相同!! 請確認讀卡機或pin碼!!')
                last_digi_num = now_digi_num

            # input the pin
            doc_pin = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['digiquery_pin'])))
            if doc_pin.text != vs_id_pw['pin']:
                doc_pin.clear()
                doc_pin.send_keys(vs_id_pw['pin'])
            
            # choose and click the signing button
            try:
                digiquery_btn = temp_wait.until(EC.visibility_of_element_located((By.ID, url_dict['digiquery_ie_btn'])))
                # if HCAServiSign exists, click PCSC button
                if checkIfProcessRunning(config_dict['HCA_service_name']):
                    drivertype = driver.capabilities['browserName']
                    if drivertype in ['MicrosoftEdge', 'chrome']:
                        digiquery_btn = temp_wait.until(EC.visibility_of_element_located((By.ID, url_dict['digiquery_chrome_btn'])))
                sleep(10)
                driver.execute_script('arguments[0].click()', digiquery_btn)
                sleep(0.5)
                waitPageLoad(driver)
            except Exception as error:
                raise ValueError('批次簽章digiquery_btn設定錯誤!! %s' % error)
            
            # 如果有延遲簽章的對話框, 就選擇臨床業務繁忙, 按下確認
            try:
                DDL_reason = temp_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, url_dict['digiback_ddl_reason']))) # wait for 3 seconds
                if DDL_reason:
                    try:
                        DDL_reason.click()
                        sleep(0.5)
                        DDL_confirm = temp_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, url_dict['digiback_ddl_confirm'])))
                        DDL_confirm.click()
                        sleep(0.5)
                    except TimeoutException: # WebDriverWait throws TimeoutException if it fails
                        raise ValueError('批次簽章選擇延遲簽章原因失敗!!')
            except:
                pass

            # pause for 3 minutes
            sleep(180)
            looptime += 1

    except Exception as error:
        raise ValueError('批次簽章設定錯誤!! %s' % error)
    
    finally:
        try:
            driver.quit()
        except:
            pass