from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

main_url = 'https://hh.ru'
page = '/vacancies/data-scientist?page=0'

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/101.0.4951.64 Safari/537.36'}
while(True):
    try:
        response = requests.get(main_url+page, headers=headers)

        with open('page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)

        with open('page.html', 'r', encoding='utf-8') as f:
            html = f.read()

        soup = bs(html, 'html.parser')

        vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})
        page = soup.find('a', {'class': 'bloko-button', 'data-qa': 'pager-next'}).get('href')

        def get_vacancies(vacancies):
            all_vacancy = []
            for vacancy in vacancies:
                vacancy_info = {}

                vacancy_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()
                vacancy_link = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']

                if vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}):
                    salary_split = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText().split()
                    vacancy_salary_currency = salary_split[-1]
                    if len(salary_split) == 6: # (220000 – 230000 руб)
                        vacancy_salary_min = int(''.join(map(str, salary_split[0:2])))
                        vacancy_salary_max = int(''.join(map(str, salary_split[3:5])))
                    if len(salary_split) == 4: # (от/до 380000 руб)
                        if salary_split[0] == 'от':
                            vacancy_salary_min = int(''.join(map(str, salary_split[1:3])))
                            vacancy_salary_max = None
                        if salary_split[0] == 'до':
                            vacancy_salary_min = None
                            vacancy_salary_max = int(''.join(map(str, salary_split[1:3])))
                    if len(salary_split) == 3: # (270000 руб)
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

            pprint(all_vacancy)

        get_vacancies(vacancies)
    except:
        get_vacancies(vacancies)
        break
