import psycopg2
from psycopg2.extensions import connection as psycopg2_connection

import os

from dotenv import load_dotenv

from src.hh_ru_parsing_vacancies import Vacancies

from src.hh_ru_parsing_employers import Employers


class SqlConnection:
    """ подключение к базе данных и добавление элементов в таблицы, удаление таблиц """
    load_dotenv()  # Загружаем переменные окружения из файла .env

    HOST = os.getenv('HOST')
    DATABASE = os.getenv('DATABASE')
    DB_USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('PASSWORD')

    # Атрибут для хранения соединения
    connection: psycopg2_connection = None

    # отфильтрованные списки
    reform_employers: list = list()
    reform_vacancies: list = list()

    def __init__(self, list_employers: list, list_vacancies: list):
        self.list_employers = list_employers
        self.list_vacancies = list_vacancies

    @classmethod
    def sql_connection(cls):
        """ подключение к бд """
        # подключение к базе данных
        if cls.connection is None:
            cls.connection = psycopg2.connect(
                host=cls.HOST,
                database=cls.DATABASE,
                user=cls.DB_USER,
                password=cls.PASSWORD
            )
            return cls.connection
        else:
            return f'Соединение установлено'

    @classmethod
    def build_tables(cls):
        """ проектирование таблиц """
        with cls.connection.cursor() as cur:
            # составление запросов, execute query

            # таблица для работодателя
            cur.execute('''CREATE TABLE Employers(
                        employer_id SERIAL PRIMARY KEY, 
                        name VARCHAR(50),
                        alternate_url VARCHAR(255))''')

            # таблица для вакансий
            cur.execute('''CREATE TABLE Vacancies(
                        employer_id int,
                        vacancy_name VARCHAR(255),
                        salary_from int,
                        salary_to int,
                        vacancy_url VARCHAR(255),
                        FOREIGN KEY (employer_id) REFERENCES Employers(employer_id))''')  # связь с внешним ключем id

            # Подтверждаем изменения
            cls.connection.commit()

    def data_reform_vacancies(self):
        """ трансформация данных vacancies """
        # чистим зарплату от None
        for elements in self.list_vacancies:
            for element in elements['items']:
                if element['salary'] is None:
                    element['salary'] = {'from': 0, 'to': 0, 'currency': 'RUR', 'gross': False}
                elif element['salary']['from'] is None:
                    element['salary']['from'] = 0
                elif element['salary']['to'] is None:
                    element['salary']['to'] = 0
                SqlConnection.reform_vacancies.append(element)
                SqlConnection.reform_employers = self.list_employers

    @staticmethod
    def add_data_in_tables():
        """ добавление данных в таблицу """
        if SqlConnection.connection is None:
            SqlConnection.sql_connection()  # Устанавливаем соединение, если его нет

        # добавляем данные в employers
        with SqlConnection.connection.cursor() as cur:
            for emp in SqlConnection.reform_employers:
                cur.execute("INSERT INTO employers VALUES (%s, %s, %s)", (emp['id'], emp['name'], emp['alternate_url']))
            for vac in SqlConnection.reform_vacancies:
                cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s)",
                            (vac['employer']['id'], vac['name'], vac['salary']['from'], vac['salary']['to'],
                             vac['alternate_url']))

        # Подтверждаем изменения
        SqlConnection.connection.commit()

    @classmethod
    def drop_tables(cls):
        """ удаление таблиц """
        if cls.connection is None:
            cls.sql_connection()  # Устанавливаем соединение, если его нет

        with cls.connection.cursor() as cur:
            cur.execute('''
                DROP TABLE IF EXISTS Vacancies;
                DROP TABLE IF EXISTS Employers;
                ''')

        # Подтверждаем изменения
        cls.connection.commit()

    # # закрываем курсор
    # cur.close()
    #
    # connection.close()
    #
    # # connection.commit()


a = SqlConnection(Employers.json_employers, Vacancies.json_vacancies)

a.sql_connection()
# a.build_tables()
# a.data_reform_vacancies()
# a.add_data_in_tables()

a.drop_tables()
# print(a)



