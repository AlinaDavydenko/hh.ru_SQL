import requests

from src.abstract_classes import ParsingVacancies

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
