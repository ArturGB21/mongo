from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
vacancies = db.vacancies
usd = 72.48
eur = 83.59

min_value_rub = int(input('Введите минимальную сумму зарплаты:'))

for vacancy in vacancies.find(
        {'$or':
            [
                {'currency': 'руб.',
                    '$or':
                        [
                            {'min_value': {'$gt': min_value_rub}},
                            {'max_value': {'$gt': min_value_rub}}
                        ]
                },
                {'currency': 'USD',
                     '$or':
                        [
                            {'min_value': {'$gt': min_value_rub/usd}},
                            {'max_value': {'$gt': min_value_rub/usd}}
                        ]
                },
                {'currency': 'EUR',
                     '$or':
                        [
                            {'min_value': {'$gt': min_value_rub/eur}},
                            {'max_value': {'$gt': min_value_rub/eur}}
                        ]
                }
            ]
        }
)

pprint(vacancy)

