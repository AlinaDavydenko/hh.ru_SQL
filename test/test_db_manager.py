import unittest
from unittest.mock import patch, MagicMock
from psycopg2.extensions import connection as psycopg2_connection
from src.db_manager import DBManager  # Замените на правильный путь


class TestDBManager(unittest.TestCase):

    @patch.object(DBManager, 'connection', autospec=True)
    def test_get_companies_and_vacancies_count(self, mock_connection):
        """Тестируем метод get_companies_and_vacancies_count."""

        # Мокируем курсор
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Мокируем результат запроса
        mock_cursor.fetchall.return_value = [
            ("Company A", 5),
            ("Company B", 3)
        ]

        # Создаем экземпляр класса
        db_manager = DBManager("word1", "word2", mock_connection)

        # Выполняем метод
        result = db_manager.get_companies_and_vacancies_count()

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, [("Company A", 5), ("Company B", 3)])

        # Проверка вызова SQL-запроса
        mock_cursor.execute.assert_called_with('''
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

    @patch.object(DBManager, 'connection', autospec=True)
    def test_get_all_vacancies(self, mock_connection):
        """Тестируем метод get_all_vacancies."""

        # Мокируем курсор
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Мокируем результат запроса
        mock_cursor.fetchall.return_value = [
            ("Company A", "Software Developer", 50000, 70000, "url1"),
            ("Company B", "Data Scientist", 60000, 80000, "url2")
        ]

        # Создаем экземпляр класса
        db_manager = DBManager("word1", "word2", mock_connection)

        # Выполняем метод
        result = db_manager.get_all_vacancies()

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, [
            ("Company A", "Software Developer", 50000, 70000, "url1"),
            ("Company B", "Data Scientist", 60000, 80000, "url2")
        ])

    @patch.object(DBManager, 'connection', autospec=True)
    def test_get_avg_salary(self, mock_connection):
        """Тестируем метод get_avg_salary."""

        # Мокируем курсор
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Мокируем результат запроса
        mock_cursor.fetchall.return_value = [
            ("Company A", 60000),
            ("Company B", 70000)
        ]

        # Создаем экземпляр класса
        db_manager = DBManager("word1", "word2", mock_connection)

        # Выполняем метод
        result = db_manager.get_avg_salary()

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, [("Company A", 60000), ("Company B", 70000)])

    @patch.object(DBManager, 'connection', autospec=True)
    def test_get_vacancies_with_higher_salary(self, mock_connection):
        """Тестируем метод get_vacancies_with_higher_salary."""

        # Мокируем курсор
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Мокируем результат запроса
        mock_cursor.fetchall.return_value = [
            ("Software Developer", 70000, 90000, "url1", "Company A"),
            ("Data Scientist", 80000, 100000, "url2", "Company B")
        ]

        # Создаем экземпляр класса
        db_manager = DBManager("word1", "word2", mock_connection)

        # Выполняем метод
        result = db_manager.get_vacancies_with_higher_salary()

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, [
            ("Software Developer", 70000, 90000, "url1", "Company A"),
            ("Data Scientist", 80000, 100000, "url2", "Company B")
        ])

    @patch.object(DBManager, 'connection', autospec=True)
    def test_get_vacancies_with_keyword(self, mock_connection):
        """Тестируем метод get_vacancies_with_keyword."""

        # Мокируем курсор
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Мокируем результат запроса
        mock_cursor.fetchall.return_value = [
            ("Software Developer", 70000, 90000, "url1", "Company A"),
            ("Data Scientist", 80000, 100000, "url2", "Company B")
        ]

        # Создаем экземпляр класса
        db_manager = DBManager("Developer", "Data", mock_connection)

        # Выполняем метод
        result = db_manager.get_vacancies_with_keyword()

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, [
            ("Software Developer", 70000, 90000, "url1", "Company A"),
            ("Data Scientist", 80000, 100000, "url2", "Company B")
        ])

        # Проверяем вызов SQL-запроса
        mock_cursor.execute.assert_called_with(f'''
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
                v.vacancy_name ILIKE '%' || 'Developer' || '%' 
                OR v.vacancy_name ILIKE '%' || 'Data' || '%';
            ''')


if __name__ == '__main__':
    unittest.main()
