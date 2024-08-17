import sys
from functools import wraps
import shlex
from typing import Callable, List
from address_book import AddressBook, ADDRESS_BOOK_FIELDS
from field import Birthday, Date
from notes_book import Notebook, NOTES_BOOK_FIELDS
from record import Record, Phone, Name
from note import Note
from serialization import save_data, load_contacts, load_notes
from views.TextView import ErrorView, WarningView, InfoView


def input_error(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError, KeyError) as e:
            ErrorView(f"[{func.__name__}] {str(e)}\n").output()
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
            ErrorView(str(e)).output()


def get_record_by_name(args: list, address_book: AddressBook) -> Record:
    if len(args) < 1:
        raise ValueError("Missing name as argument")
    
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
def delete_contact(args: list, address_book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Not enough arguments. Input: delete-contact <name>")

    name = ' '.join(args)
    if not address_book.find(name):
        raise ValueError(f"Contact with name {name} does not exist.")

    address_book.delete(name)
    return f"Contact with name {name} deleted"

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
    InfoView(f"Editing contact: {record.name.value}").output()

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
def show_all(address_book: AddressBook):
    address_book.search("")

@input_error
def show_all(notes_book: Notebook) -> str:
    notes_book.search("")


@input_error
def get_contacts_by_birthdate(args: list, address_book: AddressBook):
    if len(args) == 0:
        raise ValueError("Not enough arguments. Input: get-contacts-by-birthdate to:[dd.mm.yyyy] from:[dd.mm.yyyy]")

    to_date = from_date = None

    for arg in args:
        res = arg.split(':')
        if len(res) != 2 or res[0] not in ["to", "from"]:
            raise ValueError("Incorrect input. Input: get-contacts-by-birthdate to:[dd.mm.yyyy] from:[dd.mm.yyyy]")

        to_date = Date(res[1]) if res[0] == "to" else to_date
        from_date = Date(res[1]) if res[0] == "from" else from_date

    address_book.search_by_date(from_date, to_date)

@input_error
def search_name(args: list, address_book: AddressBook):
    search(args, address_book, ADDRESS_BOOK_FIELDS.NAME)

@input_error
def search_address(args: list, address_book: AddressBook):
    search(args, address_book, ADDRESS_BOOK_FIELDS.ADDRESS)

@input_error
def search_email(args: list, address_book: AddressBook):
    search(args, address_book, ADDRESS_BOOK_FIELDS.EMAIL)

@input_error
def search_phone(args: list, address_book: AddressBook):
    search(args, address_book, ADDRESS_BOOK_FIELDS.PHONE)

@input_error
def search_tags(args: list, notes_book: Notebook):
    search(args, notes_book, NOTES_BOOK_FIELDS.TAGS)

@input_error
def search_body(args: list, notes_book: Notebook):
    search(args, notes_book, NOTES_BOOK_FIELDS.BODY)

@input_error
def search_title(args: list, notes_book: Notebook):
    search(args, notes_book, NOTES_BOOK_FIELDS.TITLE)

@input_error
def search_notes_all_fields(args: list, notes_book: Notebook):
    search(args, notes_book, NOTES_BOOK_FIELDS.ALL)

@input_error
def search_contacts_all_fields(args: list, address_book: AddressBook):
    search(args, address_book, ADDRESS_BOOK_FIELDS.ALL)

def search(args: list, book: Notebook | AddressBook, field: ADDRESS_BOOK_FIELDS | NOTES_BOOK_FIELDS):
    # TODO: code smells should be handled with commands class
    sort = direction = ""
    if len(args) == 0:
        raise ValueError("Not enough arguments. Input: search[-entity] [keyword] [sort]:[field]:[direction]")
    if len(args) > 1:
        sort_commands = args[1].split(":")
        if sort_commands[0] != "sort":
            raise ValueError(f"Sort command {sort_commands[0]} is not supported")
        sort = "" if len(sort_commands) < 2 else sort_commands[1]
        direction = "" if len(sort_commands) < 3 else sort_commands[2]

    book.search(args[0], field, sort, direction)

@input_error
def birthdays(args, address_book: AddressBook) -> None:
    if len(args) == 0:
        return address_book.get_upcoming_birthdays()
    if len(args) == 1:
        try:
            days = int(args[0])
            return address_book.get_upcoming_birthdays(days_prior=days)
        except Exception as e:
            ErrorView(str(e)).output()
            raise ValueError("Wrong format! Command is birthdays [days_forward] (parameter is optional, default is 7 days)")
    else:
        raise ValueError("Wrong format! Command is birthdays [days_forward] (parameter is optional, default is 7 days)")


@input_error
def add_note(args: list, notes_book: Notebook) -> str:
    if len(args) < 1:
        raise ValueError("Not enough arguments. Input: add-note \"<title>\"")

    note = Note()
    note.title = ' '.join(args)
    note.body = input("Enter body: ")
    note.tags = input("Enter tags separated by comma: ").split(",")

    notes_book.add_note(note)
    return f"Added {note}"


@input_error
def show_notes(notes_book: Notebook):
    notes_book.search("")


@input_error
def edit_note(args: list, notes_book: Notebook) -> str:
    if len(args) < 1:
        raise ValueError("Not enough arguments. Input: edit-note \"<title>\"")

    title = ' '.join(args)
    note = notes_book.get_note_by_title(title)
    if note is None:
        current_notes_list = "\n".join([str(note) for note in notes_book.get_notes()])
        return f"Can't find a note with title {title}. Current notes: \n{current_notes_list}"

    # Populate a fresh Note with values to update the existing one
    new_note = Note()
    new_note.title = input(f"Enter new title (current: {note.title}): ")
    new_note.body = input(f"Enter new body (current: {note.body}): ")
    current_tags = ",".join(note.tags)
    new_note.tags = input(f"Enter new tags (current: {current_tags}): ").split(",")

    notes_book.update_note(note, new_note)
    return f"Edited note {note}"

@input_error
def remove_note(args: list, notes_book: Notebook) -> str:
    if len(args) < 1:
        raise ValueError("Not enough arguments. Input: remove-note \"<title>\"")

    title = ' '.join(args)
    notes_book.remove_note(title)
    return f"Removed note with title {title}"


def parse_input(input_str: str) -> tuple:
    command, *args = shlex.split(input_str)
    command = command.strip().lower()
    return command, *args


def main():
    if sys.version_info[0:2] != (3, 12):
        ErrorView('Sorry, app requires Python 3.12, please consult with a Readme file about the setup instructions').output()
        sys.exit(1)

    address_book = load_contacts()
    notes_book = load_notes()
    InfoView("Welcome to the assistant bot!").output()
    while True:
        input_str = input("Enter command: ")
        command, *args = parse_input(input_str)

        match command:
            case "hello":
                InfoView("How can I help you?").output()
            case "add":
                print(add_contact(args, address_book))
            case "delete-contact":
                print(delete_contact(args, address_book))
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
                show_all(address_book)
                show_all(notes_book)
            case "birthdays":
                print(birthdays(args, address_book))
            case "search-contacts":
                search_contacts_all_fields(args, address_book)
            case "search-name":
                search_name(args, address_book)
            case "search-phone":
                search_phone(args, address_book)
            case "search-email":
                search_email(args, address_book)
            case "search-address":
                search_address(args, address_book)
            case "add-note":
                print(add_note(args, notes_book))
            case "edit-note":
                print(edit_note(args, notes_book))
            case "delete-note":
                print(remove_note(args, notes_book))
            case "all-notes":
                show_notes(notes_book)
            case "search-notes":
                search_notes_all_fields(args, notes_book)
            case "search-tag":
                search_tags(args, notes_book)
            case "search-title":
                search_title(args, notes_book)
            case "search-body":
                search_body(args, notes_book)
            case "get-contacts-by-birthdate":
                get_contacts_by_birthdate(args, address_book)
            case "exit" | "quit" | "close":
                break
            case _:
                WarningView("Invalid command.").output()

    save_data(address_book)
    save_data(notes_book, filename="notes.pkl")
    InfoView("Good bye!").output()


if __name__ == "__main__":
    main()
