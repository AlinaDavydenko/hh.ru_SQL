import unittest
from unittest.mock import patch, MagicMock
from src.settings import employers
from src.hh_ru_parsing_employers import Employers  # Замените на правильный путь к вашему модулю


class TestEmployers(unittest.TestCase):

    @patch('requests.get')
    def test_get_employers_by_id_success(self, mock_get):
        """Тестируем успешное получение данных о работодателях."""

        # Мокируем успешный ответ от API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 12345, "name": "Company A"}

        mock_get.return_value = mock_response

        # Словарь с ID работодателей
        employers_dict = {
            "company_1": "12345",
            "company_2": "67890"
        }

        # Создаем экземпляр класса
        employers_instance = Employers(employers_dict)

        # Получаем данные
        result = employers_instance.get_employers_by_id()

        # Проверяем, что данные были добавлены в json_employers
        self.assertEqual(len(result), 1)  # Должен быть один элемент, так как только один успешный запрос
        self.assertEqual(result[0], {"id": 12345, "name": "Company A"})

        # Проверка вызова requests.get с правильным URL
        mock_get.assert_called_with(url='https://api.hh.ru/employers/12345')

    @patch('requests.get')
    def test_get_employers_by_id_error(self, mock_get):
        """Тестируем ошибку при запросе к API."""

        # Мокируем ошибочный ответ от API (например, статус 404)
        mock_response = MagicMock()
        mock_response.status_code = 404

        mock_get.return_value = mock_response

        # Словарь с ID работодателей
        employers_dict = {
            "company_1": "12345",
            "company_2": "67890"
        }

        # Создаем экземпляр класса
        employers_instance = Employers(employers_dict)

        # Выполняем запрос
        result = employers_instance.get_employers_by_id()

        # Проверяем, что возвращена ошибка с кодом 404
        self.assertEqual(result, 'Ошибка 404')

        # Проверка вызова requests.get с правильным URL
        mock_get.assert_called_with(url='https://api.hh.ru/employers/12345')

    @patch('requests.get')
    def test_get_employers_by_id_empty_dict(self, mock_get):
        """Тестируем случай, когда словарь работодателей пуст."""

        # Мокируем успешный ответ от API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 12345, "name": "Company A"}

        mock_get.return_value = mock_response

        # Создаем экземпляр класса с пустым словарем
        employers_dict = {}

        employers_instance = Employers(employers_dict)

        # Выполняем запрос
        result = employers_instance.get_employers_by_id()

        # Проверяем, что результат пуст
        self.assertEqual(result, [])

        # Проверка, что запрос не был выполнен, так как словарь пустой
        mock_get.assert_not_called()


if __name__ == '__main__':
    unittest.main()
