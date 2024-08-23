import json
import chromedriver_autoinstaller_fix

# modified from tbrowndev/EdgeWebDriverUpdater
import subprocess, os, requests
from shutil import Error, copy
from zipfile import ZipFile, BadZipFile
from pathlib import Path
from requests.exceptions import RequestException

# customized functions
from lib.sys_initial import initialConfig, initialUrl
from lib.sys_func import saveFile

def isEdgeWebDriverUpdated(driver_path):
    browser_version = '125.0.2535.92'
    driver_version = ''
    try:
        browser_version = subprocess.run(["powershell.exe", "(Get-AppxPackage -Name 'Microsoft.MicrosoftEdge.Stable').Version"], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        driver_version = subprocess.run([os.path.join(Path().resolve(), driver_path, 'msedgedriver.exe'), "-version"], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    except:
        pass
    return browser_version, driver_version

def updateEdgeWebDriver(version: str, driver_path):
    updateUrl = f'https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip'
    downloads_folder = os.path.join(Path().resolve(), driver_path)
    downloadFile = os.path.join(downloads_folder, 'driver_update.zip')
    try:
        # download zip file to downloads folder
        res = requests.get(updateUrl, allow_redirects=True)
        open(downloadFile, 'wb').write(res.content)
    
        # unzip file into web driver folder
        ZipFile(downloadFile, 'r').extract('msedgedriver.exe', driver_path)
    
        # remove zip file
        os.remove(downloadFile)
    except (RequestException, BadZipFile, Error, OSError) as e:
        print(f'Failed to get {version} update. Manual update is needed:\n', e)
    return driver_path

def checkUpdate(driver_path):
    browser_version, driver_version = isEdgeWebDriverUpdated(driver_path)
    if browser_version:
        if browser_version not in driver_version:
            driver_path = updateEdgeWebDriver(browser_version, driver_path)
    return driver_path

def webDriverUpdate(browser, driver_path):
    try:
        driver_path = driver_path.rsplit(sep="\\", maxsplit=1)[0]
        if browser == 'chrome':
            try:
                download_path = chromedriver_autoinstaller_fix.install(path=driver_path)
                copy(download_path, os.path.join(Path().resolve(), driver_path, 'chromedriver.exe'))
                os.remove(download_path)
            except:
                print(f'Failed to get chrome driver update. Manual update is needed:\n')
            driver_path = os.path.join(driver_path, 'chromedriver.exe')
        elif browser == 'edge':
            driver_path = checkUpdate(driver_path)
            driver_path = os.path.join(driver_path, 'msedgedriver.exe')
        return driver_path
    except Exception as error:
        raise ValueError('sys_update: webDriverUpdate 錯誤!! %s' % error)

def updateWebDriver(config_dict):
    try:
        config_dict['edge_driver_path'] = webDriverUpdate('edge', config_dict['edge_driver_path'])
        config_dict['chrome_driver_path'] = webDriverUpdate('chrome', config_dict['chrome_driver_path'])
        return config_dict
    except Exception as error:
        raise ValueError('sys_update: updateWebDriver 錯誤!! %s' % error)

def updateConfigKey(config_dict, url_dict):
    new_config_dict = initialConfig()
    for key, value in new_config_dict.items():
        if key not in config_dict:
            config_dict[key] = value
    config_path = 'sys\\config.json'
    config_data = json.dumps(config_dict, ensure_ascii=False)
    saveFile(config_path, config_data)

    new_web_config_dict = initialUrl()
    for key, value in new_web_config_dict.items():
        if key not in url_dict:
            url_dict[key] = value
    web_config_data = json.dumps(url_dict, ensure_ascii=False)
    saveFile(config_dict['url_path'], web_config_data)
    return config_dict, url_dict