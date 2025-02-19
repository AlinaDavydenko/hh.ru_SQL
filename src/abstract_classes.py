from abc import ABC, abstractmethod


class ParsingVacancies(ABC):
    """ абстракный класс для класса Vacancies """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies_by_id(self):
        pass


class ParsingEmployers(ABC):
    """ абстракный класс для класса Employers """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_employers_by_id(self):
        pass
