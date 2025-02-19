# файл для парсинга данных о работодателях
import requests

from src.abstract_classes import ParsingEmployers

from src.settings import employers


class Employers(ParsingEmployers):
    """ класс для получения данных о работодателях по их id """
    json_employers: list = []

    def __init__(self, employers_dict: dict):
        self.employers_dict = employers_dict

    def get_employers_by_id(self):
        """ получение данных о работодателях по id """
        for key, value in self.employers_dict.items():
            url = f"https://api.hh.ru/employers/{employers[key]}"
            data = requests.get(url=url)
            if data.status_code == 200:
                Employers.json_employers.append(data.json())
            else:
                return f'Ошибка {data.status_code}'
        return Employers.json_employers
