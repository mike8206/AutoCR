from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

# customized functions
from lib.wait_page_load import wait_page_load

def chkPtBtn(pt_tag_ele):
    color = pt_tag_ele.value_of_css_property('backgroundColor')
    if color in ('orangered', 'hotpink'):
        return True
    else:
        return False

def clinic_credit(driver, url_dict, session_id, vscredclinic):
    driver.get(url_dict['open_clinic_url'] + session_id)
    driver.minimize_window()
    wait_page_load(driver)
    
    # vscredclinic = {'clinicarg': clinic_arg, 'credvsid': credid, 'cliniclist': choosenclinic}
    clinic_arg = vscredclinic['clinicarg']

    # select clinic
    Select(driver.find_element(By.ID, url_dict['clinic_hosp_list'])).select_by_visible_text(clinic_arg['HOSP'])
    Select(driver.find_element(By.ID, url_dict['clinic_dept_list'])).select_by_visible_text(clinic_arg['DEPT'])
    Select(driver.find_element(By.ID, url_dict['clinic_ampm_list'])).select_by_visible_text(clinic_arg['AMPM'])
    year_input_ele = driver.find_element(By.ID, url_dict['clinic_year'])
    month_input_ele = driver.find_element(By.ID, url_dict['clinic_month'])
    day_input_ele = driver.find_element(By.ID, url_dict['clinic_day'])
    year_input_ele.clear()
    month_input_ele.clear()
    day_input_ele.clear()
    year_input_ele.send_keys(clinic_arg['YEAR'])
    month_input_ele.send_keys(clinic_arg['MONTH'])
    day_input_ele.send_keys(clinic_arg['DAY'])
    driver.find_element(By.ID, url_dict['clinic_query_btn']).click()
    wait_page_load(driver)

    # loop over all clinic
    clinic_list = vscredclinic['cliniclist']
    for clinic in clinic_list:
        try:
            clinic_tag_ele = driver.find_element(By.ID, clinic)
            if clinic_tag_ele:
                clinic_tag_ele.click()
                wait_page_load(driver)
                driver.find_element(By.ID, url_dict['clinic_all_pt_btn']).click()
                wait_page_load(driver)
                number = 0
                strNum = str(number).zfill(2)
                ptBTN = url_dict['clinic_pt_prefix']+strNum+url_dict['clinic_pt_suffix']
                try:
                    pt_tag_ele = driver.find_element(By.ID, ptBTN)
                    if chkPtBtn(pt_tag_ele):
                        ptBTN.click()
                        wait_page_load(driver)
                        # 開檔
                        if 'MedicalManagementAuthor.aspx' in driver.current_url:
                            driver.find_element(By.ID, 'RBList').click()
                            driver.find_element(By.ID, 'ConfirmButton').click()
                            wait_page_load(driver)
                        # 修改申報
                        driver.find_element(By.ID, url_dict['clinic_ptpage_other_func']).click()
                        wait_page_load(driver)
                        driver.find_element(By.ID, url_dict['clinic_ptpage_change_cred']).click()
                        wait_page_load(driver)
                        cred_input_ele = driver.find_element(By.ID, url_dict['clinic_cred_input'])
                        cred_input_ele.clear()
                        cred_input_ele.send_keys(vscredclinic['credvsid'])
                        driver.find_element(By.ID, url_dict['clinic_cred_change_btn']).click()
                        wait_page_load(driver)
                        driver.find_element(By.ID, url_dict['clinic_cred_return_pt']).click()
                        wait_page_load(driver)
                        driver.find_element(By.ID, url_dict['clinic_ptpage_return']).click()
                except:
                    continue
        except:
            continue
    driver.quit()