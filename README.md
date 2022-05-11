# AutoCR

## 更新部分
* 新增簽章、開診、寄簡訊功能
* 模組化設定
* 可自定義網址元素
* 初次設定提醒
* 重定向檔案結構
> 將chromedriver, IEDriverServer32放在sys目錄下
> 將驗證碼寫入檔案，便於ddddocr讀取

* 整合自動登入帳號密碼+簽章清單
> LoginID.txt 架構為三行，去除前綴字典key碼

------
## 預計更新
1. 更新驗證碼程式
2. 自動登入
3. 自動改績效

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
pyinstaller A.spec
```
