# AutoCR

## 簡介
為減輕在各寶山行政壓力，在學長姐們的傳承下，此軟體因此誕生!!

## 特別感謝
感謝 *哲瑞學長、孟馨老公*及*前輩*的努力!!

## 功能特色
1. 自動簽章
2. 自動開診
3. 自動寄簡訊
4. 一鍵改績效
5. 一鍵請假異動確認
6. 初次設定檔案檢查
7. 模組化設計
8. 可自定義網址元素
------
## 更新部分
v1.2.0 - 1.5.1
* 更新檔案目錄
* 合併改績效功能、客製化簡訊內容
* 使用webdriver manager簡化更新webdriver問題
* 使用FreeSimpleGUI替代PySimpleGUI

v1.1.1
* 更新檔案目錄
* 修正IE native event造成開診中斷
* 修正Google日曆因全日活動造成簡訊失敗

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
## Troubleshoot
1. 目前開診仍未能讀取讀卡機，推測可能為網頁載入完成時ajax未完全讀取，問題解決方式可能為延長秒數、更新判斷網頁載入完成機制等。
2. 目前 ddddocr 受限於 onnxruntime ，僅支援 Python version <=3.10
3. pyinstaller無法執行，可使用以下指令檢查安裝位置
```
pip uninstall pyinstaller
```
4. 其他錯誤可在sys\\error_log.txt查詢
------
## 預計更新
* 修正開診部分
------
## 使用前注意事項
1. CR或VS登入文字檔架構為三行
2. 若不想加入Google行事曆預設primary，可至sys\\sys_config.json設定
------
## 打包方式
1. 安裝以下程式
```
pip install -r requirements.txt
```
2. 依照自己電腦安裝package的位置，更新spec檔案內pathx變數：
> pathex=['C:\\python.3.9\\localcache\\local-packages'],
3. 將ddddocr在python package內的common.onnx檔案複製到與spec相同目錄下，並更新spec檔案：
> datas=[('.\\common.onnx', 'ddddocr'), ('.\\common_old.onnx', 'ddddocr')],
4. 在AutoCR.py及AutoCR.spec資料夾內打開終端，使用指令pyinstaller打包成exe檔
```
pyinstaller AutoCR.spec
```
------
## 數位簽章
(參考: https://ithelp.ithome.com.tw/articles/10281279
及 https://shuwn.dev/2021/12/02/python_exe_%E5%9F%B7%E8%A1%8C%E6%AA%94%E4%B8%A6%E9%80%B2%E8%A1%8C%E7%A8%8B%E5%BC%8F%E7%B0%BD%E7%AB%A0/)
1. 準備自然人憑證
2. 在網路上下載signtool.exe
3. 輸入指令使用signtool新增電子憑證進exe檔
```
C:\signtool.exe sign /a /t http://timestamp.sectigo.com /fd SHA256 /v C:\Users\Desktop\test\test.exe
```
1. 輸入自然人憑證Pin碼
2. 出現以下訊息即為新增憑證成功
```
Number of files successfully Signed: 1
Number of warnings: 0
Number of errors: 0
```