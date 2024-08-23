from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# customized functions
from lib.sys_web import waitPageLoad

def transferDigisign(driver, url_dict, session_id, vs_id_pw, dlist):
    unsignlist = []
    try:
        temp_wait = WebDriverWait(driver, 300)
        click_wait = WebDriverWait(driver, 15)

        # go to digisign replace url
        driver.get(url_dict['digisign_replace_url'] + session_id)
        driver.minimize_window()
        
        # loop through list of doctors and change the digisign
        list_length = len(dlist)
        for i in range(0, list_length):
            waitPageLoad(driver)
            doctor_id = list(dlist.keys())[i]
            if doctor_id == vs_id_pw['id']:
                continue
            else:
                driver.refresh()
                digi_doc_id = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['digi_doc_id'])))
                digi_doc_id.send_keys(doctor_id)
                digi_doc_id.send_keys(Keys.ENTER)
                waitPageLoad(driver)
                
                txbEmpNO = temp_wait.until(EC.text_to_be_present_in_element_value((By.ID, url_dict['digi_doc_id']), str(doctor_id)))
                if txbEmpNO == True:
                    while True:
                        waitPageLoad(driver)
                        try:
                            refresh_btn_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['digi_refresh_btn'])))
                            refresh_btn_ele.click()
                            break
                        except:
                            continue
                    waitPageLoad(driver)
                    show_of_digisign = temp_wait.until(EC.text_to_be_present_in_element((By.ID, url_dict['digi_count_text']), '筆'))
                    if show_of_digisign:
                        num_of_digisign = temp_wait.until(EC.visibility_of_element_located((By.ID, url_dict['digi_count_text'])))
                        # skip if nothing to sign
                        if num_of_digisign.text == '0筆':
                            continue
                        else:
                            # select all digisign items
                            checkbox_checked = False
                            while checkbox_checked == False:
                                try:
                                    EMR_cbx = click_wait.until(EC.element_to_be_clickable((By.ID, url_dict['digi_EMR_cbx']))) # 醫囑/病歷紀錄
                                    driver.execute_script('arguments[0].click()', EMR_cbx)
                                    checkbox_checked = True
                                except:
                                    try:
                                        DRUG_cbx = click_wait.until(EC.element_to_be_clickable((By.ID, url_dict['digi_DRUG_cbx']))) # 給藥紀錄
                                        driver.execute_script('arguments[0].click()', DRUG_cbx)
                                        checkbox_checked = True
                                    except:
                                        continue

                            while True:
                                new_doc_id = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['digi_new_id'])))
                                new_doc_id.send_keys(vs_id_pw['id'])
                                new_doc_id.send_keys(Keys.ENTER)
                                
                                waitPageLoad(driver)
                                txbEmpNoNew = temp_wait.until(EC.text_to_be_present_in_element_value((By.ID, url_dict['digi_new_id']), str(vs_id_pw['id'])))
                                if txbEmpNoNew == True:
                                    try:
                                        waitPageLoad(driver)
                                        nameEmpNew = temp_wait.until(EC.visibility_of_element_located((By.ID, url_dict['digi_new_name']))).text
                                        if nameEmpNew:
                                            try:
                                                tran_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['digi_tran_btn'])))
                                                tran_btn.click()
                                                break
                                            except:
                                                continue
                                    except:
                                        continue
                                try:
                                    new_doc_id.clear()
                                except:
                                    pass
                            
                            # Handle alert if present, otherwise continue
                            try: 
                                waitPageLoad(driver)
                                temp_wait.until(EC.alert_is_present())
                                alert = driver.switch_to.alert
                                alert.accept()
                            except:
                                continue
                            
                            show_of_digisign = temp_wait.until(EC.text_to_be_present_in_element((By.ID, url_dict['digi_count_text']), '筆'))
                            if show_of_digisign:
                                num_of_digisign = temp_wait.until(EC.visibility_of_element_located((By.ID, url_dict['digi_count_text'])))
                                if  num_of_digisign.text != '0筆':
                                    unsignlist.append(doctor_id)
                    else:
                        continue
                else:
                    continue
            waitPageLoad(driver)
        return unsignlist
    
    except Exception as error:
        raise ValueError('transferDigisign 設定錯誤!! %s' % error)
    
    finally:
        try:
            driver.quit()
        except:
            pass