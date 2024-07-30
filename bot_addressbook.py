from typing import List, Dict
import sys
import os
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        return value.isdigit() and len(value) == 10

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False


# Декоратор для обробки помилок
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone."
        except IndexError:
            return "Invalid command format. Use: add [name] [phone], change [name] [new_phone], phone [name]"
    return inner

# Додавання контакту з обробкою помилок
@input_error
def add_contact(address_book: AddressBook, args: str) -> str:
    parts = args
    name = parts[0]
    phones = parts[1:]
    if not name or not phones:
        raise ValueError
    record = address_book.find(name)
    if not record:
        record = Record(name)
        address_book.add_record(record)
    for p in phones:
        record.add_phone(p)
    return "Contact added."

# Зміна контакту з обробкою помилок
@input_error
def change_contact(address_book: AddressBook, name: str, old_phone: str, new_phone: str) -> str:
    record = address_book.find(name)
    if record and record.edit_phone(old_phone, new_phone):
        return "Contact updated."
    return "Contact not found."

# Показати номер телефону контакту з обробкою помилок
@input_error
def show_phone(address_book: AddressBook, name: str) -> str:
    record = address_book.find(name)
    if record:
        return ', '.join(phone.value for phone in record.phones)
    return "Contact not found."

# Показати всі контакти з обробкою помилок
@input_error
def show_all(address_book: AddressBook) -> str:
    if address_book:
        return "\n".join([str(record) for record in address_book.values()])
    return "No contacts found."

# Видалення контакту з обробкою помилок
@input_error
def remove_contact(address_book: AddressBook, name: str) -> str:
    if address_book.delete(name):
        return "Contact removed."
    return "Contact not found."

# Парсинг вводу користувача
def parse_input(user_input: str) -> (str, List[str]):
    parts = user_input.strip().split(maxsplit=3)
    command = parts[0].lower()
    args = parts[1:]
    return command, args

def main():
    address_book = AddressBook()
    while True:
        user_input = input("Menu:\n1- add\n2- change \n3- phone \n4- all \n5- remove\nEnter command: ")
        command, args = parse_input(user_input)

        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(address_book, args))
        elif command == "change":
            print(change_contact(address_book, *args))
        elif command == "phone":
            print(show_phone(address_book, *args))
        elif command == "all":
            print(show_all(address_book))
        elif command == "remove":
            print(remove_contact(address_book, *args))
        elif command in ("exit", "close"):
            print("Good bye!")
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()