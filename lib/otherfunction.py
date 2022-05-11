import win32com.client as com
from lib.wait_page_load import wait_page_load
from lib.solve_captcha import solve_captcha
import PySimpleGUI as sg

def auto_ie_ocr(url_dict):
    layout = [[
        [sg.Text('自動填驗證碼: 檢核網址中...')],
        [sg.Text('', key='-URL-', size=(100,1))],
        [sg.Push(),sg.Button('結束', key='-EXIT-'),sg.Push()]
    ]]
    while True:
        event, values = sg.Window('自動填驗證碼', layout).read(close=True)
        if event == '-EXIT-' or sg.WIN_CLOSED:
            break
        else:
            shellwindows_guid = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'
            for ie in com.Dispatch(shellwindows_guid):
                try:
                    document = ie.Document
                    values['-URL-'].update(document.URL)
                    if document and (url_dict['portal_url']).lower() in document.URL.lower():
                        wait_page_load(ie)
                        captcha_input_ele = [input_ele
                            for input_ele in ie.Document.body.all.tags('input')
                            if input_ele.id == url_dict['captcha_input_ele'][1:]][0]
                        # Stop immediately if the captcha has already been filled
                        if captcha_input_ele.value == '':
                            captcha_img_ele = [img
                                for img in ie.Document.body.all.tags('img')
                                if img.id == url_dict['captcha_img_ele'][1:]][0]
                            captcha = solve_captcha(captcha_img_ele)
                            captcha_input_ele.value = captcha
                        else:
                            continue
                    else:
                        continue
                except AttributeError:
                    continue