import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

# S ='30,000 元/月'
# price = S.strip().split(' ')[1]
# print(price)
url = 'https://rent.591.com.tw/rent-detail-10990210.html'
resp = requests.get(url)
bs = BeautifulSoup(resp.text,'lxml')


title = bs.find(class_='houseInfoTitle').text
print(title)
# price = bs.find(class_='price clearfix').text.split(' ')[0]
# print(price)

attr_info = bs.find(class_= 'attr').findAll('li')
labelList = bs.find(class_= 'labelList-1').findAll('li')

# print(labelList)
# print(attr_info)


for attr in attr_info:
    attr = attr.text.replace(u'\xa0','')
    # print(attr)
    if '坪數' in attr:
        sqm = attr.split(':')[1]
        # print(sqm)
        
for label in labelList:
    label = re.sub(r"\s+", "", label.text)
    # print(label)
    if '車位' in label:
        print(label.split('：')[1])
    