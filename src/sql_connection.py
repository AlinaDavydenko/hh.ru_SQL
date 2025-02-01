import psycopg2
from psycopg2.extensions import connection as psycopg2_connection

import os

from dotenv import load_dotenv


class SqlConnection:
    """ подключение к базе данных и добавление элементов в таблицы """
    load_dotenv()  # Загружаем переменные окружения из файла .env

    HOST = os.getenv('HOST')
    DATABASE = os.getenv('DATABASE')
    DB_USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('PASSWORD')

    # Атрибут для хранения соединения
    connection: psycopg2_connection = None

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
                        alternate_url VARCHAR(255),
                        open_vacancies int)''')

            # таблица для вакансий
            cur.execute('''CREATE TABLE Vacancies(
                        employer_id int PRIMARY KEY,
                        vacancy_name VARCHAR(50),
                        salary_from int,
                        salary_to int,
                        vacancy_url VARCHAR(255),
                        FOREIGN KEY (employer_id) REFERENCES Employers(employer_id))''')  # связь с внешним ключем id

            # Подтверждаем изменения
            cls.connection.commit()

    def drop_tables(self):
        pass

# заполнить в таблицу данные

    #             rows = cur.fetchall()
    #             cur.execute('DROP TABLE vacancy')
    #
    # for row in rows:
    #     print(row)
    #
    # # закрываем курсор
    # cur.close()
    #
    # connection.close()
    #
    # # connection.commit()


list1 = []
list2 = []
a = SqlConnection(list1, list2)
a.sql_connection()
# a.build_tables()
print(a)
