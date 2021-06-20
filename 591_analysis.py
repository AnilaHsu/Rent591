from os import write
import requests
from bs4 import BeautifulSoup
import MySQLdb
import re
import os


db = MySQLdb.connect(host="127.0.0.1", user="simple",
                     passwd="123456789", db="rent591")
cursor = db.cursor()

SQL = 'select * from url'
cursor.execute(SQL)
urls = cursor.fetchall()
# os.remove("error.txt")


def log(text):
    with open("error.txt", 'a') as f:
        f.write(str(text))

def getData(url):
    resp = requests.get('https:'+ url)

    if resp.status_code == 200:
        bs = BeautifulSoup(resp.text, 'html.parser')

        title = None
        price = None
        layout = None
        sqm = None
        floor = None
        house_type = None
        house_status = None
        community = None
        pet = None
        prkg = None
        cooking = None
        id_req = None

        title = bs.find(class_='houseInfoTitle')
        if (title == None):
            log("No content: {}\n".format(url))
            return {}

        title = title.text

        price = bs.find(class_='price clearfix').text.split(' ')[0]

        labelList = bs.find(class_='labelList-1').find_all('li')
        attr_info = bs.find(class_='attr').find_all('li')

        for attr in attr_info:
            attr = attr.text.replace(u'\xa0', '')
            if '格局' in attr:
                layout = attr.split(':')[1]
            elif '坪數' in attr:
                sqm = attr.split(':')[1]
            elif '樓層' in attr:
                floor = attr.split(':')[1]
            elif '型態' in attr:
                house_type = attr.split(':')[1]
            elif '現況' in attr:
                house_status = attr.split(':')[1]
            elif '社區' in attr:
                community = attr.split(':')[1]

        for label in labelList:
            label = re.sub(r"\s+", "", label.text)

            if '養寵物' in label:
                pet = label.split('：')[1]
            elif '車位' in label:
                prkg = label.split('：')[1]
            elif '開伙' in label:
                cooking = label.split('：')[1]
            elif '身份要求' in label:
                id_req = label.split('：')[1]

        return {'title':title,'price':price,'layout': layout, 'sqm': sqm, 'floor': floor, 'house_type': house_type, 'house_status': house_status, 'community': community,'pet':pet,'prkg':prkg,'cooking':cooking,'id_req':id_req}

    else:
        log("404 URL: {}\n".format(url))
        return {}

for url in urls:
    url = url[0]
    url = url.replace(' ','') 
    data_dict = getData(url)
    print(data_dict)
    if len(data_dict) == 0:
        pass
    else:
        placeholders = ', '.join(['%s']* len(data_dict))  
        columns = ', '.join(data_dict.keys())   
        insert_sql =  "INSERT INTO rent591 ( %s ) VALUES ( %s )" % (columns, placeholders)
        cursor.execute(insert_sql, data_dict.values())
        db.commit()

