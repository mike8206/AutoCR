from requests import get
import ddddocr

headers={
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
}

def downloadFile(url):
    response = get(url, headers=headers)
    img_bytes = response.content
    return img_bytes

def solve_captcha(captcha_img_ele):
    img_bytes = downloadFile(captcha_img_ele.get_attribute('src'))
    ocr = ddddocr.DdddOcr()
    captcha = ocr.classification(img_bytes)
    return captcha