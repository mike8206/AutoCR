#!/usr/bin/env python
# coding: utf-8

#!/bin/env python3
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import ddddocr

# url base
BASE_URL = 'http://portal.ntuh.gov.tw/General/Login.aspx'
digisign_replace_url = 'http://ihisaw.ntuh.gov.tw/WebApplication/DigitalSignature/DSExecuteEmpReplace.aspx?SESSION='
digisign_background_url = 'http://ihisaw.ntuh.gov.tw/WebApplication/DigitalSignature/BackGroundDS.aspx?SESSION='

# file path
credential_path = "loginID.txt"
list_path = "List.txt"
image_path = 'temp.gif'

# options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')

TIMEOUT = 5
headers={
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
}

# read portal credential from txt file
d = {}
with open(credential_path) as f:
    idpwpin = f.read().splitlines()
f.close()
d['id']=idpwpin[0]
d['pw']=idpwpin[1]
d['pin']=idpwpin[2]
d # id pw pin (帳號 密碼 PIN碼)

# read doctor list from txt file (for digital signature)
dlist = {}
with open(list_path, encoding="ANSI") as f:
    for line in f:
        (key, val) = line.split()
        dlist[key] = val
dlist


def download_file(url):
    response = requests.get(url, headers=headers)
    with open(image_path, 'wb') as f:
        f.write(response.content)

def wait_page_load(driver):
    wait = WebDriverWait(driver, timeout=TIMEOUT)
    try:
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        return True
    except TimeoutException:
        return False

def solve_captcha(captcha_img_ele):
    download_file(captcha_img_ele.get_attribute('src'))
    ocr = ddddocr.DdddOcr()
    with open(image_path, 'rb') as f:
        img_bytes = f.read()
    captcha = ocr.classification(img_bytes)
    return captcha

def start(driver): # go to NTUH portal homepage
    driver.get(BASE_URL)
    wait_page_load(driver) 
    
    # find all elements needed
    username_input_ele = driver.find_element_by_css_selector('#txtUserID')
    password_input_ele = driver.find_element_by_css_selector('#txtPass')
    captcha_img_ele = driver.find_element_by_css_selector('#imgVerifyCode')
    captcha_input_ele = driver.find_element_by_css_selector('#txtVerifyCode')
    submit_ele = driver.find_element_by_css_selector('#imgBtnSubmitNew')
    
    # solve captcha and login with credential
    username_input_ele.send_keys(d['id'])
    password_input_ele.send_keys(d['pw'])
    captcha = solve_captcha(captcha_img_ele)
    captcha_input_ele.send_keys(captcha)
    # print('captcha = ' + captcha)
    time.sleep(1.5)
    
    submit_ele.click()
    wait_page_load(driver) 
    
    # return the session id
    session_id = get_session_id(driver)
    return session_id
    
def get_session_id(driver):
    # get session id
    current_url = driver.current_url
    split_url = current_url.split("SESSION=")
    session_id = split_url[1]
    # print("session id = " + session_id)
    return session_id

def run(driver, session_id):    
    # go to digisign replace url
    driver.get(digisign_replace_url + session_id)
    
    # loop through list of doctors and change the digisign
    list_length = len(dlist)
    for i in range(0, list_length):    
        doctor_id = list(dlist.keys())[i]
        print("doctor id = " + list(dlist.keys())[i] + "; doctor name = " + list(dlist.values())[i])

        driver.refresh()
        driver.find_element_by_css_selector('#NTUHWeb1_txbEmpNO').send_keys(doctor_id)
        wait_page_load(driver) 

        driver.find_element_by_css_selector('#NTUHWeb1_UpdatePanel1').click()
        time.sleep(2)
        wait_page_load(driver) 

        driver.find_element_by_css_selector('#NTUHWeb1_btnRefresh').click()
        time.sleep(2)
        wait_page_load(driver) 
        
        # print number of digisign
        num_of_digisign = ''
        while num_of_digisign == '':
            try: 
                num_of_digisign = driver.find_element_by_css_selector('#NTUHWeb1_lblUnDsCnts').text
                print(num_of_digisign)
                time.sleep(1)
            except:
                print("number of digisign not fetched")
                break
        
        # skip if nothing to sign
        if  num_of_digisign == '0筆':
            continue
        
        # select all digisign items
        checkbox_checked = False
        while checkbox_checked == False:
            try: 
                driver.find_element_by_id('NTUHWeb1_dgrEmrRecord_ctl01_cbxSelectAll').click() # 醫囑/病歷紀錄
                checkbox1=driver.find_element_by_css_selector('#NTUHWeb1_dgrEmrRecord_ctl01_cbxSelectAll').is_selected()
                # print(checkbox1)
                if(checkbox1==True):
                    checkbox_checked = True
                # print(checkbox_checked)
                print("all items selected")
            except:
                try:
                    driver.find_element_by_id('NTUHWeb1_dgrDrugGivenRecord_ctl01_cbxSelectAll').click() # 給藥紀錄 (2021.04.10 revise)
                    checkbox2=driver.find_element_by_css_selector('#NTUHWeb1_dgrDrugGivenRecord_ctl01_cbxSelectAll').is_selected()
                    # print(checkbox2)
                    if(checkbox2==True):
                        checkbox_checked = True            
                    # print(checkbox_checked)
                    print("all items selected")
                except:
                    # print(checkbox_checked)
                    print("not yet selected all items")      
        time.sleep(1.5)
        wait_page_load(driver) 
        
        # input the new ID to replace old ones
        driver.find_element_by_css_selector('#NTUHWeb1_txbEmpNoNew').send_keys(d['id'])
        time.sleep(1.5)
        wait_page_load(driver) 

        # click the button to replace
        driver.find_element_by_css_selector('#NTUHWeb1_btnUpdate').click()
        time.sleep(1.5)
        
        # check for alert
        try: 
            alert = driver.switch_to.alert
            alertText = alert.text
            print("ERROR: (ALERT BOX DETECTED) - ALERT MSG : " + alertText)
            alert.accept()
            print("alert accepted")
        except:
            # print("no alert")
            continue
            
def background_sign(driver_ie, session_id):
    # IE goto digisign page for background signing
    driver_ie.get(digisign_background_url + session_id)
    time.sleep(1)
    wait_page_load(driver_ie) 

    # input the pin
    driver_ie.find_element_by_css_selector('#NTUHWeb1_txbPinCode').send_keys(d['pin'])
    time.sleep(1)
    wait_page_load(driver_ie) 

    # click the signing button
    driver_ie.find_element_by_css_selector('#NTUHWeb1_btnBackGroundDSByPCSC').click()
    time.sleep(1)
    wait_page_load(driver_ie) 
    
    # 如果有延遲簽章的對話框, 就選擇臨床業務繁忙, 按下確認
    try:
        DDL_reason = WebDriverWait(driver_ie, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#reasonDDL-id > option:nth-child(1)"))) # wait for 3 seconds
        DDL_reason.click()
        time.sleep(0.5)
        DDL_confirm = driver_ie.find_element_by_css_selector("body > div > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(1)")
        DDL_confirm.send_keys(Keys.RETURN)
        time.sleep(0.5)
        print("DDL reason checked.")
    except TimeoutException: # WebDriverWait throws TimeoutException if it fails
        print("no DDL prompt.")
    
    # sleep for 5 mins
    print('sleep for 5 mins')
    time.sleep(300)
    driver_ie.quit()
    
    
def main():
    # chrome driver
    # driver = webdriver.Chrome(options = chrome_options)
    driver = webdriver.Chrome("chromedriver.exe",options = chrome_options)
    driver.implicitly_wait(TIMEOUT)
    # login using chrome and get the session id
    session_id = start(driver)
    # use chrome for digisign replacing all IDs
    run(driver, session_id)
    # IE driver
    driver_ie = webdriver.Ie("IEDriverServer32.exe")
    driver_ie.implicitly_wait(TIMEOUT)
    # open IE for background signing
    background_sign(driver_ie, session_id)

if __name__ == '__main__':
    main()