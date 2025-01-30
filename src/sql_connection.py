import psycopg2

import os

from dotenv import load_dotenv


class SqlConnection:
    """ подключение к базе данных и добавление элементов в таблицы """
    load_dotenv()
    HOST = os.getenv('HOST')
    DATABASE = os.getenv('DATABASE')
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')

    def __init__(self, list_employers: list, list_vacancies: list):
        self.list_employers = list_employers
        self.list_vacancies = list_vacancies

    @classmethod
    def sql_connection(cls):
        """ подключение к бд и проектирование таблиц """
        # подключение к базе данных
        with psycopg2.connect(
            host=cls.HOST,
            database=cls.DATABASE,
            user=cls.USER,
            password=cls.PASSWORD
        ) as connection:
            with connection.cursor() as cur:
                # составление запросов, execute query

                # таблица для работодателя
                cur.execute('CREATE TABLE Employers('
                            'employer_id int PRIMARY KEY, '
                            'name VARCHAR(50),'
                            'alternate_url VARCHAR(255),'
                            'open_vacancies int)')

                # таблица для вакансий
                cur.execute('CREATE TABLE Vacancies('
                            'employer_id int PRIMARY KEY,'
                            'vacancy_name VARCHAR(50),'
                            'salary_from int,'
                            'salary_to int,'
                            'vacancy_url,'
                            'FOREIGN KEY (employer_id) REFERENCES Employers(employer_id))')  # связь с внешним ключем id

                connection.commit()

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
