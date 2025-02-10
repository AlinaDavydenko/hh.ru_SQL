from psycopg2.extensions import connection as psycopg2_connection


class DBManager:
    """ класс для работы с данными БД """
    # Атрибут для хранения соединения
    avg_salary: int = 0

    def __init__(self, word1: str, word2: str, connection: psycopg2_connection):
        self.word1 = word1
        self.word2 = word2
        self.connection = connection

    def get_companies_and_vacancies_count(self):
        """ получает список всех компаний и количество вакансий у каждой компании """
        with self.connection.cursor() as cur:
            cur.execute('''
            SELECT 
                e.employers_name,
                COUNT(v.vacancy_name) AS vacancy_count
            FROM 
                Employers e
            LEFT JOIN 
                Vacancies v ON e.employer_id = v.employer_id
            GROUP BY 
                e.employers_name;
                ''')

            rows = cur.fetchall()
            return rows

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
        with self.connection.cursor() as cur:
            cur.execute('''
            SELECT 
                e.employers_name,
                AVG((v.salary_from + v.salary_to) / 2) AS average_salary
            FROM 
                Employers e
            JOIN 
                Vacancies v ON e.employer_id = v.employer_id
            GROUP BY 
                e.employers_name;''')

            rows = cur.fetchall()
            return rows

    def get_vacancies_with_higher_salary(self):
        """ получает список всех вакансий, у которых зарплата выше средней по всем вакансиям """
        with self.connection.cursor() as cur:
            cur.execute('''
            SELECT 
                v.vacancy_name,
                v.salary_from,
                v.salary_to,
                v.vacancy_url,
                e.employers_name
            FROM 
                Vacancies v
            JOIN 
                Employers e ON v.employer_id = e.employer_id
            WHERE 
                (v.salary_from + v.salary_to) / 2 > (
                    SELECT AVG((salary_from + salary_to) / 2)
                    FROM Vacancies
                );
            ''')

            rows = cur.fetchall()
            return rows

    def get_vacancies_with_keyword(self):
        """ получает список всех вакансий, в названии которых содержатся переданные в метод слова """
        with self.connection.cursor() as cur:
            cur.execute(f'''
            SELECT 
                v.vacancy_name,
                v.salary_from,
                v.salary_to,
                v.vacancy_url,
                e.employers_name
            FROM 
                Vacancies v
            JOIN 
                Employers e ON v.employer_id = e.employer_id
            WHERE 
                v.vacancy_name ILIKE '%' || '{self.word1}' || '%' 
                OR v.vacancy_name ILIKE '%' || '{self.word2}' || '%';
            ''')

            rows = cur.fetchall()
            return rows
