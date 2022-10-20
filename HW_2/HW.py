from abc import ABC, abstractmethod
import pickle


class AbstractOutput(ABC):
    """ Абстрактний базовий класс, для різних типів виводу (cli, web) """
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def output(self):
        ...


class CliOutput(AbstractOutput):
    """ Класс виводу в консоль """
    def output(self):
        return self.data


class WebOutput(AbstractOutput):
    """ Класс виводу в web """
    file_name = "Py6PersonalAssistant-main/AddressBook.bin"

    def output(self):
        with open(self.file_name, "rb") as file:
            unpacked = pickle.load(file)
            return unpacked

    def send(self):
        ...


class Connection:
    """ Класс підключення до web """
    def __init__(self):
        ...


connect = Connection()


def decorator(func):
    """ Декоратор для статичних функцій, в залежності від підключення до Web виводять інформацію в консоль чи в Web """

    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        data.__str__()
        if data:
            if connect:
                result = WebOutput(data).output().send()
                return result
            elif not connect:
                result = CliOutput(data)
                result.output()
                return result
        return wrapper