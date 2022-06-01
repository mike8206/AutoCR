# AutoCR

## 簡介
為減輕在各寶山行政壓力，在學長姐們的傳承下，此軟體因此誕生!!

## 特別感謝
感謝 *哲瑞學長、孟馨老公*及*前輩*的努力!!

## 功能特色
1. 自動簽章
2. 自動開診
3. 自動寄簡訊
4. 一鍵改績效(已改至其他專案)
5. 一鍵查電話(已改至其他專案)
6. 一鍵請假異動確認
7. 初次設定檔案檢查
8. 模組化設定
9. 可自定義網址元素
------
## 更新部分
v1.1.0
* 移除改績效、查電話功能
* 更新檔案目錄
* 修正開診錯誤(仍會中斷)
* 修正讀取檔案編碼錯誤

v1.0.7
* 新增查電話(尚未測試)
* 更新檔案目錄
* 修正簽章錯誤
* 修正開診錯誤
* 修正簡訊時間
* 修正Google日曆token
* 修正請假異動
* 將驗證碼寫入暫存檔傳遞

v1.0.6
* 新增一鍵請假異動確認
* 更新網址參數
------
## 預計更新
* 晨科會排班 (以另一專案寫code中)
* 一鍵搬影片 (尚未開始)
------
## 使用前注意事項
1. 將符合電腦版本的chromedriver, IEDriverServer32放在sys目錄下
2. 若不想加入Google行事曆預設primary，可至sys\\sys_config.txt設定
3. CR或VS登入文字檔架構為三行
------
## 打包方式
1. 安裝以下程式
```
pip install --upgrade pyinstaller selenium pySimpleGUI apscheduler pytz requests ddddocr chardet google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
2. 依照自己電腦安裝package的位置，更新spec檔案內pathx變數：
> pathex=['C:\\python.3.9\\localcache\\local-packages'],
3. 將ddddocr在python package內的common.onnx檔案複製到與spec相同目錄下，並更新spec檔案：
> datas=[('./common.onnx','ddddocr')],
4. 在AutoCR.py及AutoCR.spec資料夾內打開終端，使用指令pyinstaller打包成exe檔
```
pyinstaller AutoCR.spec
```
------
## Troubleshoot
1. 目前 ddddocr 僅支援 Python version <=3.9
2. pyinstaller無法執行，可使用以下指令檢查安裝位置
```
pip uninstall pyinstaller
```
3. 其他錯誤可在sys\\error_log.txt查詢
