import psycopg2

from psycopg2.extensions import connection as psycopg2_connection


class DBManager:
    """ класс для работы с данными БД """
    # Атрибут для хранения соединения
    avg_salary: int = 0

    def __init__(self, name_job: str, connection: psycopg2_connection):
        self.name_job = name_job
        self.connection = connection

    def get_companies_and_vacancies_count(self):
        """ получает список всех компаний и количество вакансий у каждой компании """

        pass

    def get_all_vacancies(self):
        """ получает список всех вакансий с указанием всех данных """
        with self.connection.cursor() as cur:
            cur.execute('''
            SELECT employers_name, vacancy_name, salary_from, salary_to, vacancy_url
            FROM employers
            LEFT JOIN vacancies USING(employer_id)''')

            rows = cur.fetchall()
            return rows

    def get_avg_salary(self):
        """ получает среднюю зарплату по вакансиям """
        pass

    def get_vacancies_with_higher_salary(self):
        """ получает список всех вакансий, у которых зарплата выше средней по всем вакансиям """
        pass

    def get_vacancies_with_keyword(self):
        """ получает список всех вакансий, в названии которых содержатся переданные в метод слова """
        pass
