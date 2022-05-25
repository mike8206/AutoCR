# customized functions
from lib.sys_func import readIdPwPin
from lib.web_driver_setting import web_driver_setting
from lib.login import login
from lib.digisign.digisign_transfer import digisign_transfer
from lib.digisign.digisign_background import digisign_background

def main(url_dict, vs_id_path, list_path, chrome_driver_path, ie_driver_path):
    # read portal credential from txt file
    vsidpw = {}
    try:
        vsidpw = readIdPwPin(vs_id_path)
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
    driver = web_driver_setting('chrome', chrome_driver_path, 'max')
    # login using chrome and get the session id
    session_id = login(driver, url_dict, vsidpw)
    try:
        # use chrome for digisign replacing all IDs
        digisign_transfer(driver, url_dict, session_id, vsidpw, dlist)
        driver.close()
    except Exception as error:
        driver.close()
        raise ValueError('轉簽章設定錯誤!! %s' % error)
    try:
        # IE driver
        driver_ie = web_driver_setting('ie', ie_driver_path, '')
        # open IE for background signing
        digisign_background(driver_ie, url_dict, session_id, vsidpw)
        driver_ie.close()
    except Exception as error:
        driver_ie.close()
        raise ValueError('背景簽章設定錯誤!! %s' % error)
    