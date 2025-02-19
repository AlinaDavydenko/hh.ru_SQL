import psycopg2

from psycopg2.extensions import connection as psycopg2_connection

import os

from dotenv import load_dotenv


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

    def __init__(self, database_name, list_employers: list, list_vacancies: list):
        # название будущей базы данных
        self.database_name = database_name

        # списки с работодателями и вакансиями
        self.list_employers = list_employers
        self.list_vacancies = list_vacancies

    @classmethod
    def sql_connection(cls):
        """ подключение к бд """
        if cls.connection is None or cls.connection.closed:
            cls.connection = psycopg2.connect(
                host=cls.HOST,
                database=cls.DATABASE,
                user=cls.DB_USER,
                password=cls.PASSWORD
            )
        return cls.connection

    def new_database(self):
        """ создание новой базы данных """
        self.connection.autocommit = True  # каждая строчка автоматически коммитится

        with self.connection.cursor() as cur:
            cur.execute(f'''CREATE DATABASE {self.database_name}''')
            SqlConnection.DATABASE = self.database_name

            cur.close()
            SqlConnection.connection.close()

        SqlConnection.connection = psycopg2.connect(
            host=SqlConnection.HOST,
            database=self.database_name,
            user=SqlConnection.DB_USER,
            password=SqlConnection.PASSWORD
        )

    @classmethod
    def build_tables(cls):
        """ проектирование таблиц """
        cls.sql_connection()  # Ensure connection is active

        with cls.connection.cursor() as cur:
            cur.execute('DROP TABLE IF EXISTS Vacancies;')
            cur.execute('DROP TABLE IF EXISTS Employers;')
            cur.execute('''CREATE TABLE Employers(
                                employer_id SERIAL PRIMARY KEY, 
                                employers_name VARCHAR(50),
                                alternate_url VARCHAR(255))''')

            cur.execute('''CREATE TABLE Vacancies(
                                employer_id int,
                                vacancy_name VARCHAR(255),
                                salary_from int,
                                salary_to int,
                                vacancy_url VARCHAR(255),
                                FOREIGN KEY (employer_id) REFERENCES Employers(employer_id))''')

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
        SqlConnection.sql_connection()  # Ensure connection is active

        with SqlConnection.connection.cursor() as cur:
            for emp in SqlConnection.reform_employers:
                cur.execute("INSERT INTO Employers VALUES (%s, %s, %s)",
                            (emp['id'], emp['name'], emp['alternate_url']))
            for vac in SqlConnection.reform_vacancies:
                cur.execute("INSERT INTO Vacancies VALUES (%s, %s, %s, %s, %s)",
                            (vac['employer']['id'], vac['name'], vac['salary']['from'],
                             vac['salary']['to'], vac['alternate_url']))

        SqlConnection.connection.commit()

    @classmethod
    def drop_tables(cls):
        """ удаление таблиц """
        SqlConnection.sql_connection()  # Ensure connection is active

        with cls.connection.cursor() as cur:
            cur.execute('DROP TABLE IF EXISTS Vacancies;')
            cur.execute('DROP TABLE IF EXISTS Employers;')

        cls.connection.commit()

    def drop_database(self):
        """ удаляет базу данных """
        SqlConnection.sql_connection()  # Ensure connection is active

        SqlConnection.connection.close()
        SqlConnection.connection = psycopg2.connect(
            host=SqlConnection.HOST,
            database=os.getenv('DATABASE'),
            user=SqlConnection.DB_USER,
            password=SqlConnection.PASSWORD
        )

        self.connection.autocommit = True
        with self.connection.cursor() as cur:
            cur.execute(f'''DROP DATABASE {self.database_name}''')

    def close_connection(self):
        """ закрываем коннект """
        if self.connection is not None and not self.connection.closed:
            self.connection.close()
