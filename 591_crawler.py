import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re
import math
import MySQLdb

browser = webdriver.Chrome(executable_path='./chromedriver')
browser.get('https://rent.591.com.tw/?kind=0&region=1')

browser.find_element_by_class_name('area-box-close').click()
time.sleep(3)
browser.find_element_by_class_name('statement-confirm').click()

# browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
# browser.execute_script( " arguments[0].scrollIntoView(); " , pet_checkbox)

element_to_hover_over = browser.find_element_by_class_name('other')
hover = ActionChains(browser).move_to_element(element_to_hover_over)
time.sleep(2)
hover.perform()


pet_checkbox = browser.find_element_by_id("other-pet")
pet_checkbox.click()
time.sleep(2)
total = browser.find_element_by_class_name("hasData").text
regex = re.compile(r'到(\d+,*\d*)')
match = regex.search(total)
total_pages = math.ceil(int(match.group(1).replace(',', ''))/30)

url_list = []

for i in range(0,total_pages):
    bs = BeautifulSoup(browser.page_source, 'html.parser')
    titles = bs.find_all('h3')

    for title in titles:
        url = title.find('a').get('href')
        url_list.append(url)

    time.sleep(3)
    if i < total_pages-1:
        browser.find_element_by_class_name('pageNext').click()


db = MySQLdb.connect(host="127.0.0.1", user="simple", passwd="123456789", db="rent591")
cursor = db.cursor()

for url in set(url_list):    
    try:
        SQL = 'insert into url(url) values(%s)'
        cursor.execute(SQL, [url])
        db.commit()
    except Exception as e:
        print(e)


