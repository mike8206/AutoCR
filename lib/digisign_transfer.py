
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# customized functions
from lib.wait_page_load import wait_page_load

def digisign_transfer(driver, url_dict, session_id, vsidpw, dlist):
    tempWait = WebDriverWait(driver, 300)

    # go to digisign replace url
    driver.get(url_dict['digisign_replace_url'] + session_id)
    driver.minimize_window()
    
    # loop through list of doctors and change the digisign
    list_length = len(dlist)
    for i in range(0, list_length):
        wait_page_load(driver)
        doctor_id = list(dlist.keys())[i]
        if doctor_id == vsidpw['id']:
            continue
        else:
            driver.refresh()
            txbEmpNO = ''
            driver.find_element(By.ID, url_dict['digi_doc_id']).send_keys(doctor_id)
            driver.find_element(By.ID, url_dict['digi_update_panel']).click()
            wait_page_load(driver)
            txbEmpNO = tempWait.until(EC.text_to_be_present_in_element_value((By.ID, url_dict['digi_doc_id']), str(doctor_id)))
            if txbEmpNO == True:
                while True:
                    wait_page_load(driver)
                    try:
                        refresh_btn_ele = tempWait.until(EC.element_to_be_clickable((By.ID, url_dict['digi_refresh_btn'])))
                        refresh_btn_ele.click()
                        break
                    except:
                        continue
                wait_page_load(driver)
                show_of_digisign = tempWait.until(EC.text_to_be_present_in_element((By.ID, url_dict['digi_count_text']), '筆'))
                if show_of_digisign:
                    num_of_digisign = driver.find_element(By.ID, url_dict['digi_count_text'])
                    # skip if nothing to sign
                    if  num_of_digisign.text == '0筆':
                        continue
                    else:
                        # select all digisign items
                        checkbox_checked = False
                        while checkbox_checked == False:
                            try: 
                                driver.find_element(By.ID, url_dict['digi_EMR_cbx']).click() # 醫囑/病歷紀錄
                                checkbox1=driver.find_element(By.ID, url_dict['digi_EMR_cbx']).is_selected()
                                if(checkbox1==True):
                                    checkbox_checked = True
                            except:
                                try:
                                    driver.find_element(By.ID, url_dict['digi_DRUG_cbx']).click() # 給藥紀錄 (2021.04.10 revise)
                                    checkbox2=driver.find_element(By.ID, url_dict['digi_DRUG_cbx']).is_selected()
                                    if(checkbox2==True):
                                        checkbox_checked = True            
                                except:
                                    continue
                        driver.find_element(By.ID, url_dict['digi_new_id']).send_keys(vsidpw['id'])
                        driver.find_element(By.ID, url_dict['digi_tran_btn']).click()
                        while True:
                            wait_page_load(driver)
                            txbEmpNoNew = tempWait.until(EC.text_to_be_present_in_element_value((By.ID, url_dict['digi_new_id']), str(vsidpw['id'])))
                            if txbEmpNoNew == True:
                                driver.find_element(By.ID, url_dict['digi_tran_btn']).click()
                                break
                            else:
                                continue
                        try: 
                            wait_page_load(driver)
                            tempWait.until(EC.alert_is_present())
                            alert = driver.switch_to.alert
                            alert.accept()
                        except:
                            continue
                else:
                    continue
            else:
                continue
        wait_page_load(driver)