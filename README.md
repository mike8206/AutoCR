# Digisign

## 更新部分

* 重定向檔案結構
> 將loginID, List, chromedriver, IEDriverServer32放在相同目錄下
> 將驗證碼寫入檔案，便於ddddocr讀取
```
# file path
credential_path = "loginID.txt"
list_path = "List.txt"
image_path = 'temp.gif'

# main
driver = webdriver.Chrome("chromedriver.exe",options = chrome_options)
driver_ie = webdriver.Ie("IEDriverServer32.exe")
```

* 導入ddddocr破解驗證碼
```
import ddddocr

def download_file(url):
    response = requests.get(url, headers=headers)
    with open(image_path, 'wb') as f:
        f.write(response.content)

def solve_captcha(captcha_img_ele):
    download_file(captcha_img_ele.get_attribute('src'))
    ocr = ddddocr.DdddOcr()
    with open(image_path, 'rb') as f:
        img_bytes = f.read()
    captcha = ocr.classification(img_bytes)
    return captcha
```

* 整合自動登入帳號密碼+簽章清單
> LoginID.txt 架構為三行，去除前綴字典key碼
```
# read portal credential from txt file
d = {}
with open(credential_path) as f:
    idpwpin = f.read().splitlines()
f.close()
d['id']=idpwpin[0]
d['pw']=idpwpin[1]
d['pin']=idpwpin[2]
```

## 打包方式
1. 安裝pyinstaller
2. 更新spec檔案內packages位置：
```
pathex=['C:\\python.3.9\\localcache\\local-packages'],
```
3. 將ddddocr在python package內的common.onnx檔案放置到Digisign.py相同目錄下，並更新spec檔案
```
datas=[('./common.onnx','ddddocr')],
```
4. 在Digisign.py及Digisign.spec資料夾內打開終端，使用指令pyinstaller打包成exe檔
```
pyinstaller Digisign.spec
```
