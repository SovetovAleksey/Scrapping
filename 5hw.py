'''
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные
о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=chrome_options)

driver.implicitly_wait(10)

driver.get("https://account.mail.ru/login/")

input = driver.find_element(By.XPATH, "//input[@name='username']")
input.send_keys("study.ai_172@mail.ru")

input.send_keys(Keys.ENTER)

input = driver.find_element(By.XPATH, "//input[@name='password']")
input.send_keys("NextPassword172#")

input.send_keys(Keys.ENTER)

mails = []
unique_links = set()
db_mail_ru = MongoClient('localhost', 27017)['mail_ru']
messages = db_mail_ru.messages

#num - при наводе курсора на кнопку "Входящие" высвечивается окно с информацией о количестве всех сообщений
num = driver.find_element(By.XPATH,
                          "//a[@class='nav__item js-shortcut nav__item_active nav__item_shortcut nav__item_child-level_0']").get_attribute(
    'title').split()[1]

while len(mails) < int(num):
    letters = driver.find_elements(By.XPATH,
                                   "//a[@class='llc llc_normal llc_new llc_new-selection js-letter-list-item js-tooltip-direction_letter-bottom'] | \
                                   //a[@class='llc llc_normal llc_last llc_new llc_new-selection js-letter-list-item js-tooltip-direction_letter-bottom'] | \
                                   //a[@class='llc llc_normal llc_first llc_new llc_new-selection js-letter-list-item js-tooltip-direction_letter-bottom']")
    actions = ActionChains(driver)

    for letter in letters:
        if letter.get_attribute('href') not in unique_links:
            link = letter.get_attribute('href')
            info = letter.find_element(By.CLASS_NAME, 'llc__content')
            author = info.find_element(By.CLASS_NAME, 'll-crpt').get_attribute('title')
            subject = info.find_element(By.CLASS_NAME, 'll-sj__normal').text
            date = letter.find_element(By.CLASS_NAME, 'llc__item_date').get_attribute('title')
            mail = {'author': author, 'date': date, 'subject': subject, 'link': link}
            messages.insert_one(mail)
            unique_links.add(link)

    actions.move_to_element(letters[-1])
    actions.perform()

driver.quit()
