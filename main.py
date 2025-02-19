from src.settings import employers

from src.hh_ru_parsing_employers import Employers

from src.hh_ru_parsing_vacancies import Vacancies

from src.sql_connection import SqlConnection

from src.db_manager import DBManager

# парсинг вакансий и работодателей
my_employers = Employers(employers)
my_employers.get_employers_by_id()
list_employers = Employers.json_employers  # получение списка работодателей

my_vacancies = Vacancies(employers)
my_vacancies.get_vacancies_by_id()
list_vacancies = Vacancies.json_vacancies  # получение списка вакансий

# SQL соединение и заполнение таблиц данными
sql_tables = SqlConnection('hh_ru_db', list_employers, list_vacancies)
sql_tables.sql_connection()  # соединение с базой данных
sql_tables.new_database()  # создание новой базы данных
sql_tables.build_tables()  # проектирование табличек
sql_tables.data_reform_vacancies()  # форматирование словаря с зарплатой
sql_tables.add_data_in_tables()  # добавление данных в таблицы

# класс DB_Manager, выполнение запросов
methods_vacancies = DBManager(SqlConnection.connection)

rows0 = methods_vacancies.get_all_vacancies()  # получить все данные из таблицы
for row in rows0:
    print(row)

rows1 = methods_vacancies.get_companies_and_vacancies_count()  # получение количества вакансий по каждой компании

rows2 = methods_vacancies.get_avg_salary  # получение средней зарплаты

rows3 = methods_vacancies.get_vacancies_with_higher_salary  # получение вакансий с зп выше средней

word1, word2 = input('Введите первое ключевое слово:'), input('Введите второе ключевое слово:')

rows4 = methods_vacancies.get_vacancies_with_keyword(word1, word2)  # поиск по ключевым словам

# удаление таблиц и сброс поиска
drop_it = input('Начать поиск заново? Предыдущие данные удалятся безвозвратно \n Y/N').lower()
if drop_it == 'y':
    sql_tables.drop_tables()
    sql_tables.drop_database()
    sql_tables.close_connection()
