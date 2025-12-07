# -*- coding: utf-8 -*-

import requests

import urllib
import urllib.request as ur

from PIL import Image
import pytesseract
import bs4


url='http://10.248.7.33/default2.aspx'
res = ur.urlopen(url).read()
soup = bs4.BeautifulSoup(res, 'lxml')
img = soup.find('img', id='icode')

imgurl = img.get('src')
ur.urlretrieve('http://10.248.7.33/'+imgurl, "checkcode.jpg") 

pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

test = pytesseract.image_to_string(Image.open('checkcode.jpg'))

test_data = {'uid':'080038','pwd':'zjxy2014','bdata':'2018-1-29', 'chkcode':test}
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) Gecko/20100101 Firefox/57.0',
'Host':'10.248.7.33'}

requrl = "http://10.248.7.35/WFManager/loginAction_doLogin.action"

#普通数据使用

resp = requests.session().post(url='http://10.248.7.33/default2.aspx', data=test_data, headers=header_dict)

print(resp)

