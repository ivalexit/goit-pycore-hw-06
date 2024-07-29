from typing import List, Dict
import sys
import os

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
def add_contact(contacts: Dict[str, str], name: str, phone: str) -> str:
    if not name or not phone:
        raise ValueError
    contacts[name] = phone
    return "Contact added."

# Зміна контакту з обробкою помилок

@input_error
def change_contact(contacts: Dict[str, str], name: str, new_phone: str) -> str:
    if not name or not new_phone:
        raise ValueError
    if name in contacts:
        contacts[name] = new_phone
        return "Contact updated."
    return "Contact not found."

# Показати номер телефону контакту з обробкою помилок

@input_error
def show_phone(contacts: Dict[str, str], name: str) -> str:
    if not name:
        raise ValueError
    return contacts[name]

# Показати всі контакти з обробкою помилок

@input_error
def show_all(contacts: Dict[str, str]) -> str:
    if contacts:
        return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])
    return "No contacts found."

# Парсинг вводу користувача

def parse_input(user_input: str) -> (str, List[str]):
    parts = user_input.strip().split(maxsplit=2)
    command = parts[0].lower()
    args = parts[1:]
    return command, args

def main():
    contacts = {}
    while True:
        user_input = input("Enter command: ")
        command, args = parse_input(user_input)

        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(contacts, *args))
        elif command == "change":
            print(change_contact(contacts, *args))
        elif command == "phone":
            print(show_phone(contacts, *args))
        elif command == "all":
            print(show_all(contacts))
        elif command in ("exit", "close"):
            print("Good bye!")
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()