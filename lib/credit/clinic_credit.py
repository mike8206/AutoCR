from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# customized functions
from lib.sys_web import waitPageLoad
from lib.clinic.clinic_func import clinicPageNavi

def chkPtBtn(pt_tag_ele):
    color = pt_tag_ele.value_of_css_property('color')
    # OrangeRed: rgba(255, 69, 0, 1)
    # HotPink: rgba(255, 105, 180, 1)
    # Purple: rgba(128,0,128, 1)
    if color in ('rgba(255, 69, 0, 1)', 'rgba(255, 105, 180, 1)', 'rgba(128, 0, 128, 1)'):
        return True
    else:
        return False

def modifyClinicCredit(driver, url_dict, session_id, vscredclinic):
    try:
        # vscredclinic = {'clinicarg': clinic_arg, 'credvsid': credid, 'cliniclist': choosenclinic}
        # go to clinic page
        clinic_arg = vscredclinic['clinicarg']
        clinicPageNavi(driver, url_dict, session_id, clinic_arg)

        # loop over all clinic
        temp_wait = WebDriverWait(driver, 30)
        clinic_list = vscredclinic['cliniclist']
        for clinic in clinic_list:
            clinic_tag_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, clinic)))
            if clinic_tag_ele:
                clinic_tag_ele.click()
                waitPageLoad(driver)
                clinic_all_pt = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_all_pt_btn'])))
                if clinic_all_pt.is_selected() != True:
                    clinic_all_pt.click()
                waitPageLoad(driver)
                number = 0
                while True:
                    strNum = str(number).zfill(2)
                    ptBTN = url_dict['clinic_pt_prefix']+strNum+url_dict['clinic_pt_suffix']
                    try:
                        waitPageLoad(driver)
                        pt_tag_ele = driver.find_element(By.ID, ptBTN)
                        if chkPtBtn(pt_tag_ele):
                            pt_tag_ele.click()
                            waitPageLoad(driver)
                            # 開檔
                            if url_dict['clinic_med_author'] in driver.current_url:
                                rblist = temp_wait.until(EC.element_to_be_clickable((By.NAME, url_dict['clinic_med_author_reason'])))
                                rblist[0].click()
                                ConfirmButton = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_med_author_btn'])))
                                ConfirmButton.click()
                                waitPageLoad(driver)
                            # 修改申報
                            other_func_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_ptpage_other_func'])))
                            other_func_btn.click()
                            waitPageLoad(driver)
                            
                            change_cred_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_ptpage_change_cred'])))
                            change_cred_btn.click()
                            waitPageLoad(driver)

                            cred_input_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_cred_input'])))
                            cred_input_ele.clear()
                            cred_input_ele.send_keys(vscredclinic['credvsid'])
                            cred_change_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_cred_change_btn'])))
                            cred_change_btn.click()
                            waitPageLoad(driver)

                            cred_return_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_cred_return_pt'])))
                            cred_return_btn.click()
                            waitPageLoad(driver)

                            ptpage_return_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_ptpage_return'])))
                            ptpage_return_btn.click()
                        number +=1
                    except:
                        break
                clinic_back_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_back_btn'])))
                clinic_back_btn.click()
        try:
            driver.quit()
        except:
            pass
    except Exception as error:
        driver.quit()
        raise ValueError('modifyClinicCredit: 改績效程式錯誤!! %s' % error)