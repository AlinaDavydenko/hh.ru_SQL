import unittest
from unittest.mock import patch, MagicMock
from src.hh_ru_parsing_vacancies import Vacancies  # Замените на правильный путь


class TestVacancies(unittest.TestCase):

    @patch('requests.get')
    def test_get_vacancies_by_id_success(self, mock_get):
        """Тестируем успешное получение вакансий по ID работодателей."""

        # Мокируем успешный ответ от API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"id": 1122462, "name": "Software Developer"}
            ]
        }

        mock_get.return_value = mock_response

        # Словарь с ID работодателей
        employers_dict = {
            'Skyeng': 1122462,
            'T1': 4649269
        }

        # Создаем экземпляр класса
        vacancies_instance = Vacancies(employers_dict)

        # Получаем вакансии
        result = vacancies_instance.get_vacancies_by_id()

        # Проверяем, что данные были добавлены в json_vacancies
        self.assertEqual(len(result), 2)  # Должен быть один элемент, так как только один успешный запрос
        self.assertEqual(result[0]['items'][0], {"id": 1122462, "name": "Software Developer"})

        # Проверка вызова requests.get с правильным URL
        mock_get.assert_called_with(url='https://api.hh.ru/vacancies/?employer_id=4649269')

    @patch('requests.get')
    def test_get_vacancies_by_id_error(self, mock_get):
        """Тестируем ошибку при запросе к API."""

        # Мокируем ошибочный ответ от API (например, статус 404)
        mock_response = MagicMock()
        mock_response.status_code = 404

        mock_get.return_value = mock_response

        # Словарь с ID работодателей
        employers_dict = {
            'Skyeng': 1122462,
            'T1': 4649269
        }

        # Создаем экземпляр класса
        vacancies_instance = Vacancies(employers_dict)

        # Выполняем запрос
        result = vacancies_instance.get_vacancies_by_id()

        # Проверяем, что возвращена ошибка с кодом 404
        self.assertEqual(result, 'Ошибка 404')

        # Проверка вызова requests.get с правильным URL
        mock_get.assert_called_with(url='https://api.hh.ru/vacancies/?employer_id=1122462')

    @patch('requests.get')
    def test_get_vacancies_by_id_empty_dict(self, mock_get):
        """Тестируем случай, когда словарь работодателей пуст."""

        # Мокируем успешный ответ от API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"vacancies": [{"id": 12345, "name": "Software Developer"}]}

        mock_get.return_value = mock_response

        # Создаем экземпляр класса с пустым словарем
        employers_dict = {}

        vacancies_instance = Vacancies(employers_dict)

        # Выполняем запрос
        result = vacancies_instance.get_vacancies_by_id()

        # Проверяем, что результат пуст
        self.assertEqual(result, [])

        # Проверка, что запрос не был выполнен, так как словарь пустой
        mock_get.assert_not_called()


if __name__ == '__main__':
    unittest.main()
