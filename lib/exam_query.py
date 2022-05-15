
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd

# customized functions
from lib.wait_page_load import wait_page_load

def getExamDropListEle(driver, url_dict, session_id):
    driver.get(url_dict['exam_query_url'] + session_id)
    wait_page_load(driver)
    Ampm_list = []
    Unit_list = []
    Origin_list = []
    Item_list = []
    ampm_dropdown = Select(driver.find_element(By.ID, url_dict['exam_ampm_list']))
    Ampm_list_options = ampm_dropdown.options
    unit_dropdown = Select(driver.find_element(By.ID, url_dict['exam_unit_list']))
    Unit_list_options = unit_dropdown.options
    origin_dropdown = Select(driver.find_element(By.ID, url_dict['exam_origin_list']))
    Orig_list_options = origin_dropdown.options
    item_dropdown = Select(driver.find_element(By.ID, url_dict['exam_item_list']))
    Item_list_options = item_dropdown.options

    # get all values
    for index in range(0, len(Ampm_list_options)):
        Ampm_list.append(Ampm_list_options[index].text)
    for index in range(1, len(Unit_list_options)):
        Unit_list.append(Unit_list_options[index].text)
    for index in range(0, len(Orig_list_options)):
        Origin_list.append(Orig_list_options[index].text)
    for index in range(0, len(Item_list_options)):
        Item_list.append(Item_list_options[index].text)
    
    exam_ele_values = [Ampm_list, Unit_list, Origin_list, Item_list]
    return exam_ele_values

def examGetPatientList(driver, url_dict, session_id, exam_arg):
    # exam_arg = {'AMPM','UNIT','ORIGIN','ITEM','DATE'}
    driver.get(url_dict['exam_query_url'] + session_id)
    driver.minimize_window()
    wait_page_load(driver)
    Select(driver.find_element(By.ID, url_dict['exam_ampm_list'])).select_by_visible_text(exam_arg['AMPM'])
    wait_page_load(driver)
    Select(driver.find_element(By.ID, url_dict['exam_unit_list'])).select_by_visible_text(exam_arg['UNIT'])
    wait_page_load(driver)
    Select(driver.find_element(By.ID, url_dict['exam_origin_list'])).select_by_visible_text(exam_arg['ORIGIN'])
    wait_page_load(driver)
    Select(driver.find_element(By.ID, url_dict['exam_item_list'])).select_by_visible_text(exam_arg['ITEM'])
    wait_page_load(driver)
    date_input_ele = driver.find_element(By.ID, url_dict['exam_query_date'])
    date_input_ele.clear()
    date_input_ele.send_keys(exam_arg['DATE'])
    driver.find_element(By.ID, url_dict['exam_query_btn']).click()
    wait_page_load(driver)
    # get exam table and make list
    exam_df = pd.read_html(driver.find_element(By.ID, url_dict['exam_query_table']).get_attribute('outerHTML'))[0]
    print(exam_df)

    