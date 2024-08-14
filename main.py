from functools import wraps
from typing import Callable
from address_book import AddressBook
from record import Record, Phone, Name
from serialization import save_data, load_data


def input_error(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"[{func.__name__}] {e}"
        except IndexError as e:
            return f"[{func.__name__}] {e}"
        except KeyError as e:
            return f"[{func.__name__}] {e}"
    return wrapper


def populate_field(field, func, message, allow_skip=False):
    while True:
        input_raw = input(message)
        user_input = input_raw.strip()
        if allow_skip and user_input.lower() == 'n':
            return

        try:
            if isinstance(field, list):
                input_strings = input_raw.split()
                for substring in input_strings:
                    func(substring)
                break
            else:
                func(input_raw)
                break
        except ValueError as e:
            print(e)


def get_record_by_name(args: list, address_book: AddressBook) -> Record:
    name = ' '.join(args)
    record = address_book.find(name)
    if record is None:
        raise ValueError(f"Can't find {name}")
    return record


@input_error
def add_contact(args: list, address_book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Not enough arguments. Input: add <name>")

    name = ' '.join(args)
    if address_book.find(name):
        raise ValueError(f"Contact with name {name} already exists.")

    record = Record(name)
    address_book.add_record(record)

    populate_field(record.phones, record.add_phone, "Enter phone numbers (separated by space): ")
    populate_field(record.email, record.add_email, "Enter email: ")
    populate_field(record.birthday, record.add_birthday, "Enter birthday (DD.MM.YYYY): ")
    populate_field(record.address, record.add_address, "Enter address: ")

    return f"Added {record}"

def replace_phones_on_a_contact(record, allow_skip=False):
    existing_phones = record.phones.copy()
    new_phones = []
    populate_field(record.phones, lambda phone: new_phones.append(phone), "Enter new phone numbers (separated by space) (or 'n' to skip): ", allow_skip)

    if new_phones:
        record.phones = [Phone(phone) for phone in new_phones]
    elif not new_phones and record.phones:
        record.phones = existing_phones


@input_error
def edit_phone(args: list, address_book: AddressBook) -> str:
    record = get_record_by_name(args, address_book)
    replace_phones_on_a_contact(record)
    return f"Phone number updated for {record.name.value}"


@input_error
def edit_email(args: list, address_book: AddressBook) -> str:
    record = get_record_by_name(args, address_book)
    populate_field(record.email, record.add_email, "Enter new email: ")
    return f"Email updated for {record.name.value}"


@input_error
def edit_address(args: list, address_book: AddressBook) -> str:
    record = get_record_by_name(args, address_book)
    populate_field(record.address, record.add_address, "Enter new address: ")
    return f"Address updated for {record.name.value}"


@input_error
def edit_bday(args: list, address_book: AddressBook) -> str:
    record = get_record_by_name(args, address_book)
    populate_field(record.birthday, record.add_birthday, "Enter new birthday (DD.MM.YYYY): ")
    return f"Birthday updated for {record.name.value}"


@input_error
def edit_contact(args: list, address_book: AddressBook) -> str:
    record = get_record_by_name(args, address_book)
    print(f"Editing contact: {record.name.value}")

    replace_phones_on_a_contact(record, allow_skip=True)
    populate_field(record.email, record.add_email, "Enter new email (or 'n' to skip): ", allow_skip=True)
    populate_field(record.birthday, record.add_birthday, "Enter new birthday (DD.MM.YYYY) (or 'n' to skip): ", allow_skip=True)
    populate_field(record.address, record.add_address, "Enter new address (or 'n' to skip): ", allow_skip=True)
    return f"Contact {record.name.value} updated"

@input_error
def edit_name(args: list, address_book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Not enough arguments. Input: edit-name <old_name> <new_name>")
    
    old_name = args[0]
    new_name = args[1]
    
    record = address_book.find(old_name)
    if record is None:
        return f"Can't find contact with name {old_name}"
    
    if address_book.find(new_name):
        return f"A contact with name {new_name} already exists."

    del address_book.data[old_name]
    
    record.name = Name(new_name)
    address_book.add_record(record)
    
    return f"Renamed contact {old_name} to {new_name}"

@input_error
def show_all(address_book: AddressBook) -> str:
    if address_book.data:
        return address_book
    else:
        return "No contacts"


@input_error
def add_birthday(args, address_book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Not enough arguments. Input: add-birthday <name> <birthday>")

    data = {"name": ' '.join(args[:-1]), "birthday": args[-1]}
    record = address_book.find(data["name"])
    if record is None:
        return f"Can't find {data['name']} name"

    record.add_birthday(data["birthday"])
    return f"Birthday added for {data['name']}"


@input_error
def show_birthday(args, address_book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Not enough arguments. Input: show-birthday <name>")

    name = ' '.join(args)
    record = address_book.find(name)
    if record is not None:
        return f"{name} birthday is {record.birthday}"
    return f"Can't find {name} name"


@input_error
def birthdays(args, address_book: AddressBook) -> list:
    return address_book.get_upcoming_birthdays()


def parse_input(input_str: str) -> tuple:
    command, *args = input_str.split()
    command = command.strip().lower()
    return command, *args


def main():
    address_book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        input_str = input("Enter command: ")
        command, *args = parse_input(input_str)

        match command:
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, address_book))
            case "edit-phone":
                print(edit_phone(args, address_book))
            case "edit-email":
                print(edit_email(args, address_book))
            case "edit-address":
                print(edit_address(args, address_book))
            case "edit-bday":
                print(edit_bday(args, address_book))
            case "edit-contact":
                print(edit_contact(args, address_book))
            case "edit-name":
                print(edit_name(args, address_book))
            case "all":
                print(show_all(address_book))
            case "add-birthday":
                print(add_birthday(args, address_book))
            case "show-birthday":
                print(show_birthday(args, address_book))
            case "birthdays":
                print(birthdays(args, address_book))
            case "exit" | "quit" | "close":
                break
            case _:
                print("Invalid command.")

    save_data(address_book)
    print("Good bye!")


if __name__ == "__main__":
    main()
