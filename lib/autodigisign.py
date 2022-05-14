from selenium import webdriver

# customized functions
from lib.login import login
from lib.digisign_transfer import digisign_transfer
from lib.digisign_background import digisign_background

# options
TIMEOUT = 5
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')

ie_options = webdriver.IeOptions()
ie_options.ignore_zoom_level = True
 
def main(url_dict, vs_id_path, list_path, chrome_driver_path, ie_driver_path):
    # read portal credential from txt file
    vsidpw = {}
    try:
        with open(vs_id_path, encoding="UTF-8") as f:
            idpwpin = f.read().splitlines()
        # id pw pin (帳號 密碼 PIN碼)
        vsidpw['id']=idpwpin[0]
        vsidpw['pw']=idpwpin[1]
        vsidpw['pin']=idpwpin[2]
    except:
        raise ValueError('VS帳號密碼檔案錯誤!!')

    # read doctor list from txt file (for digital signature)
    dlist = {}
    try:
        with open(list_path, encoding="UTF-8") as f:
            for line in f:
                (key, val) = line.split(' ',1)
                dlist[key] = val.removesuffix('\n')
    except:
        raise ValueError('簽章清單檔案錯誤!!')

    # chrome driver
    driver = webdriver.Chrome(chrome_driver_path, options = chrome_options)
    driver.implicitly_wait(TIMEOUT)
    # login using chrome and get the session id
    session_id = login(driver, url_dict, vsidpw)
    # use chrome for digisign replacing all IDs
    digisign_transfer(driver, url_dict, session_id, vsidpw, dlist)
    # IE driver
    driver_ie = webdriver.Ie(ie_driver_path, options = ie_options)
    driver_ie.implicitly_wait(TIMEOUT)
    # open IE for background signing
    digisign_background(driver_ie, url_dict, session_id, vsidpw)