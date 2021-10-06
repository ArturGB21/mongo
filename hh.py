# https://hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=python&search_field=description
import requests
from bs4 import BeautifulSoup as bs
import json
from pprint import pprint
from pymongo import MongoClient

def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

search_text = input("Введите вакансию")

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
hh = db.hh

def append_data_db(database, data):
    if not doc.find({'link': data.get('link')}):
        database.insert_one(data)


url = 'https://hh.ru'
params = {'fromSearchLine': 'true',
          'st': 'searchVacancy',
          'text': 'search_text',
          'search_field': 'description'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
vacancy_number = 1
page = 0

while True:
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')

    vacancy_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
    button_next = soup.find_all('a', text='дальше')


    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_name_info = vacancy.find('a', attrs={'class': 'bloko-link'})
        vacancy_name = vacancy_name_info.text

        vacancy_link = vacancy_name_info['href']

        salary = vacancy.find('span', atters={'data-qa':'vacancy-serp__vacancy-compensation'})
        if not salary:
            salary_min = None
            salary_max = None
            salary_currency = None
        else:
            salary = salary.getText()\
                .replase(u'\xa0', u'')
            salary = re.split(r'\s|<|>', salary)

            if salary[0] == 'до':
                salary_min = None
                if isinstance(salary[1]) and isinstance(salary[2]):
                    salary_max = int("".join([salary[1], salary[2]]))
                    salary_currency = salary[3]
                else:
                    salary_max = int(salary[1])
                    salary_currency = salary[2]

            elif salary[0] == 'от':
                if isinstance(salary[1]) and isinstance(salary[2]):
                    salary_min = int("".join([salary[1], salary[2]]))
                    salary_currency = salary[3]
                else:
                    salary_min = int(salary[1])
                    salary_currency = salary[2]
                salary_max = None
            else:
                if isinstance(salary[0]) and isinstance(salary[1]):
                    salary_min = int("".join([salary[0], salary[1]]))
                    if isinstance(salary[3]) and isinstance(salary[4]):
                        salary_max = int("".join([salary[3], salary[4]]))
                        salary_currency = salary[5]
                    else:
                        salary_max = int(salary[3])
                        salary_currency = salary[4]
                else:
                    salary_min = int(salary[0])
                    if isinstance(salary[2]) and isinstance(salary[3]):
                        salary_max = int("".join([salary[2], salary[3]]))
                        salary_currency = salary[3]


        vacancy_data['vacancy_number'] = vacancy_number
        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['salary_min'] = salary_min
        vacancy_data['salary_max'] = salary_max
        vacancy_data['salary_currency'] = salary_currency
        vacancy_data['site'] = url

        vacancy_number += 1

        append_data_db(hh, vacancy_data)

    if not button_next or not response.ok:
        break

    page += 1
    params = {'fromSearchLine': 'true',
          'st': 'searchVacancy',
          'text': 'search_text',
          'search_field': 'description',
          'page': 'page'}

