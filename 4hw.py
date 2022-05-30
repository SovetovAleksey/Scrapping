from lxml import html
from pprint import pprint
import requests
import datetime
from pymongo import MongoClient

url = 'https://yandex.ru/news/'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36'}
months = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
          'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)

items = dom.xpath(
        "//div[@class='mg-grid__col mg-grid__col_xs_6'] | //div[@class='mg-grid__col mg-grid__col_xs_4']")

list_items = []

for item in items:
    date = item.xpath(
        ".//div/div[contains (@class,'mg-card-footer')]/div/div/span[@class='mg-card-source__time']/text()")[0]
    d = datetime.datetime.now()

    if len(date) == 5:  # '18:43'
        date = f'{date}-{d.strftime("%d-%m-%Y")}'
    elif date.split()[0] == 'вчера':  # вчера в 15:38
        date = f"{date.split()[2]}-{(d - datetime.timedelta(days=1)).strftime('%d-%m-%Y')}"
    else:  # 28 февраля в 23:44
        date_list = date.split()
        date_list[1] = months[date_list[1]]
        date = '-'.join([date_list[-1], date_list[0], date_list[1], d.year])

    item_info = {}
    item_info['name'] = item.xpath(".//div[@class='mg-card__text-content']/div/h2/a/text()")[0].replace('\xa0', ' ')
    item_info['source'] = item.xpath(".//span[@class='mg-card-source__source']/a/text()")[0]
    item_info['link'] = item.xpath(".//span[@class='mg-card-source__source']/a/@href")[0]
    item_info['date'] = date

    list_items.append(item_info)

pprint(list_items)

client = MongoClient('localhost', 27017)
db_news_list = client['db_news_list']
news = db_news_list.news

news.insert_many(list_items)

