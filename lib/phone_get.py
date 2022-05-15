from selenium.webdriver.common.by import By
from pandas import DataFrame as df

# customized functions
from lib.wait_page_load import wait_page_load

def phone_get(driver, url_dict, session_id, patientlist):
    driver.get(url_dict['query_pt_url'] + session_id)
    driver.minimize_window()
    wait_page_load(driver)
    all_patient = []

    # patientlist = []
    for chartnumber in patientlist:
        chart_input_ele = driver.find_element(By.ID, url_dict['query_chart_ele'])
        chart_input_ele.clear()
        chart_input_ele.send_keys(chartnumber)
        driver.find_element(By.ID, url_dict['query_btn']).click()
        wait_page_load(driver)
        if 'QueryModifyPatBase.aspx?' in driver.current_url:
            sur_name = driver.find_element(By.ID, url_dict['query_pt_cht_sur']).get_property('value')
            given_name = driver.find_element(By.ID, url_dict['query_pt_cht_given']).get_property('value')
            area_code = driver.find_element(By.ID, url_dict['query_pt_areacode']).get_property('value')
            tel = driver.find_element(By.ID, url_dict['query_pt_tel']).get_property('value')
            mobile = driver.find_element(By.ID, url_dict['query_pt_mobile']).get_property('value')
            values = [chartnumber,sur_name+given_name,area_code+'-'+tel,mobile]
            all_patient.append(values)
            driver.find_element(By.ID, url_dict['query_home_btn']).click()
            wait_page_load(driver)        
    
    column_name=['病歷號', '姓名', '市話', '手機號碼']
    patient_list = df(all_patient, columns=column_name)
    patient_list.to_csv('phone_output.csv')