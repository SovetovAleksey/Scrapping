from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient

main_url = 'https://hh.ru'
page = '/vacancies/data-scientist?page=0'

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/101.0.4951.64 Safari/537.36'}
all_vacancy = []

while(True):

    response = requests.get(main_url + page, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})

    def get_vacancies(vacancies):
        for vacancy in vacancies:
            vacancy_info = {}

            vacancy_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()
            vacancy_link = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']

            if vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}):
                salary_split = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText().split()
                vacancy_salary_currency = salary_split[-1]
                if len(salary_split) == 6:  # (220000 – 230000 руб)
                    vacancy_salary_min = int(''.join(map(str, salary_split[0:2])))
                    vacancy_salary_max = int(''.join(map(str, salary_split[3:5])))
                if len(salary_split) == 4:  # (от/до 380000 руб)
                    if salary_split[0] == 'от':
                        vacancy_salary_min = int(''.join(map(str, salary_split[1:3])))
                        vacancy_salary_max = None
                    if salary_split[0] == 'до':
                        vacancy_salary_min = None
                        vacancy_salary_max = int(''.join(map(str, salary_split[1:3])))
                if len(salary_split) == 3:  # (270000 руб)
                    vacancy_salary_min = int(''.join(map(str, salary_split[0:2])))
                    vacancy_salary_max = int(''.join(map(str, salary_split[0:2])))
            else:
                vacancy_salary_min = None
                vacancy_salary_max = None
                vacancy_salary_currency = None

            vacancy_info['Name'] = vacancy_name
            vacancy_info['Salary Min'] = vacancy_salary_min
            vacancy_info['Salary Max'] = vacancy_salary_max
            vacancy_info['Salary Currency'] = vacancy_salary_currency
            vacancy_info['Link'] = vacancy_link
            vacancy_info['Site'] = main_url

            all_vacancy.append(vacancy_info)

        #pprint(all_vacancy)
        #print(len(all_vacancy))

    get_vacancies(vacancies)

    try:
        page = soup.find('a', {'class': 'bloko-button', 'data-qa': 'pager-next'}).get('href')
    except:
        print('Вакансии собраны!')
        break

'3---------------------------------------------------------------------------------------------------------------------'

client = MongoClient('127.0.0.1', 27017)

db = client['unique_vacancies']
jobs = db.jobs

unique_links = []
cnt = 0
jobs.delete_many({})

for vacancy in all_vacancy:
    if vacancy['Link'] not in unique_links:
        jobs.insert_one(vacancy)
        unique_links.append(vacancy['Link'])
    else:
        cnt += 1

#pprint(list(jobs.find({})))
print(f'Количество вакансий - {len(list(jobs.find({})))}')
print(f'Количество дублей - {cnt}')

def required_salary(number):
    for doc in list(jobs.find({'$or': [{'Salary Min': {'$gt': number}}, {'Salary Max': {'$gt': number}}]})):
        pprint(doc)

required_salary(225000)
