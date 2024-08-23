from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

# customized functions
from lib.sys_web import waitPageLoad

def countDigisignNum(driver, url_dict, session_id):
    try:
        temp_wait = WebDriverWait(driver, 300)

        # IE goto digisign page for digi amount
        driver.get(url_dict['digisign_query_url'] + session_id)
        waitPageLoad(driver)

        if not temp_wait.until(EC.text_to_be_present_in_element((By.ID, url_dict['digiquery_count_text']), '筆')):
            raise TimeoutException('讀取剩餘筆數過時!!')
        
        num_of_digisign = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['digiquery_count_text'])))
        text_digi_num = num_of_digisign.text
        left_digi = int(text_digi_num.split('筆', 1)[0])
        return left_digi
    except Exception as error:
        driver.quit()
        raise ValueError(f'讀取剩餘簽章設定錯誤!! {error}')