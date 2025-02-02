import requests

from abstract_classes import ParsingVacancies

from src.settings import employers


class Vacancies(ParsingVacancies):
    """ класс для получения всех вакансий по id работодателя """
    json_vacancies: list = []

    def __init__(self, employers_dict: dict):
        self.employers = employers_dict

    def get_vacancies_by_id(self):
        """ получаем все ваканси по id работодателей """
        for key, value in self.employers.items():
            url = f"https://api.hh.ru/vacancies/?employer_id={employers[key]}"
            data = requests.get(url=url)
            if data.status_code == 200:
                Vacancies.json_vacancies.append(data.json())
            else:
                return f'Ошибка {data.status_code}'
        return Vacancies.json_vacancies


a = Vacancies(employers)
list_of_vacancies = a.get_vacancies_by_id()

mylist = list()

for element in list_of_vacancies:
    # pprint.pprint(element['items'])
    for i in element['items']:
        if i['salary'] is None:
            i['salary'] = {'from': 0, 'to': 0, 'currency': 'RUR', 'gross': False}
        elif i['salary']['from'] is None:
            i['salary']['from'] = 0
        elif i['salary']['to'] is None:
            i['salary']['to'] = 0
        # print(i)
        mylist.append(f"{i['id']} {i['name']} {i['employer']['id']}")

# for inf in mylist:
#     print(inf)
