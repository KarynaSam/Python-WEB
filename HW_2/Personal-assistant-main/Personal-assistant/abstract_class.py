from abc import ABC, abstractmethod


class AbstractRecord(ABC):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def __str__(self):
        ...

    @abstractmethod
    def add_phone(self, phone):
        ...

    @abstractmethod
    def del_phone(self, phone):
        ...

    @abstractmethod
    def del_email(self, email):
        ...

    @abstractmethod
    def del_birthday(self, birthday):
        ...

    @abstractmethod
    def del_address(self, address):
        ...

    @abstractmethod
    def edit_phone(self, phone_num, new_phone_num):
        ...

    @abstractmethod
    def days_to_birthday(self, birthday):
        ...


class AbstractAddressBook(ABC):
    def add_record(self, record):
        ...

    def iterator(self, func=None, days=0):
        ...


class AbstractHelp(ABC):
    ...