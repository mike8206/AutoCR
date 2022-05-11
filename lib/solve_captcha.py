from requests import get
import ddddocr

image_path = 'temp.gif'

headers={
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
}

def download_file(url):
    response = get(url, headers=headers)
    with open(image_path, 'wb') as f:
        f.write(response.content)

def solve_captcha(captcha_img_ele):
    download_file(captcha_img_ele.get_attribute('src'))
    ocr = ddddocr.DdddOcr()
    with open(image_path, 'rb') as f:
        img_bytes = f.read()
    captcha = ocr.classification(img_bytes)
    return captcha