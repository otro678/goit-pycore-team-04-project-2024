import readline
import shlex
from functools import wraps
from typing import Callable, List
from address_book import AddressBook, ADDRESS_BOOK_FIELDS
from field import Birthday, Date
from notes_book import Notebook, NOTES_BOOK_FIELDS
from record import Record, Phone, Name
from note import Note
from views.TextView import ErrorView, WarningView, InfoView

def input_error(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError, KeyError) as e:
            ErrorView(f"[{func.__name__}] {str(e)}\n").output()
    return wrapper

@input_error
def show_all(books):
    for book in books:
        book.search("")

@input_error
def search(book, query, field=None, sort=None):
    fields_enum = ADDRESS_BOOK_FIELDS
    direction = "asc"
    if isinstance(book, Notebook):
        fields_enum = NOTES_BOOK_FIELDS
    if field is None:
        field = fields_enum('all')
    else:
        field = fields_enum(field.lower())
    if sort is None:
        sort = ""
    else:
        sort, direction = sort.values()
        sort = fields_enum(sort.lower())
    book.search(query, field, sort, direction)

@input_error
def add_contact(address_book, name):
    record = Record(name)
    address_book.add_record(record)
    populate_field(record.phones, record.add_phone, "Enter phone numbers (separated by space): ", allow_skip=True)
    populate_field(record.email, record.add_email, "Enter email: ", allow_skip=True)
    populate_field(record.birthday, record.add_birthday, "Enter birthday (DD.MM.YYYY): ", allow_skip=True)
    populate_field(record.address, record.add_address, "Enter address: ", allow_skip=True)
    return f"Added {record}"

@input_error
def add_note(notes_book, title):
    note = Note(title)
    note.body = input("Enter body: ")
    note.tags = input("Enter tags separated by comma: ").split(",")
    notes_book.add_note(note)
    return f"Added {note}"

@input_error
def edit_contact(address_book, name, field=None):
    record = address_book.find(name)
    if not record:
        raise ValueError(f"Contact with name {name} does not exist.")

    InfoView(f"Editing contact: {record.name.value}").output()
    if field == None or field == "Name":
        populate_field(record.name, record.edit_name, "Enter new name (or 'n' to skip): ", allow_skip=True)
    if field == None or field == "Phone":
        replace_phones_on_a_contact(record, allow_skip=True)
    if field == None or field == "Email":
        populate_field(record.email, record.add_email, "Enter new email (or 'n' to skip): ", allow_skip=True)
    if field == None or field == "Birthday":
        populate_field(record.birthday, record.add_birthday, "Enter new birthday (DD.MM.YYYY) (or 'n' to skip): ", allow_skip=True)
    if field == None or field == "Address":
        populate_field(record.address, record.add_address, "Enter new address (or 'n' to skip): ", allow_skip=True)

    return f"Contact {record.name.value} updated"

@input_error
def edit_note(notes_book, title, field=None):
    note = notes_book.get_note_by_title(title)
    if note is None:
        current_notes_list = "\n".join([str(note) for note in notes_book.get_notes()])
        return f"Can't find a note with title {title}. Current notes: \n{current_notes_list}"

    # Populate a fresh Note with values to update the existing one
    new_note = Note()
    if field == None or field == "Title":
        new_note.title = input(f"Enter new title (current: {note.title}): ")
    if field == None or field == "Body":
        new_note.body = input(f"Enter new body (current: {note.body}): ")
    current_tags = ",".join(note.tags)
    if field == None or field == "Tags":
        new_note.tags = input(f"Enter new tags (current: {current_tags}): ").split(",")

    notes_book.update_note(note, new_note)
    return f"Edited note {note}"

@input_error
def delete_contact(address_book, name):
    if not address_book.find(name):
        raise ValueError(f"Contact with name {name} does not exist.")
    address_book.delete(name)
    return f"Contact with name {name} deleted"

@input_error
def delete_note(notes_book, title):
    if not notes_book.get_note_by_title(title):
        raise ValueError(f"Note with title {title} does not exist.")
    notes_book.remove_note(title)
    return f"Removed note with title {title}"

def show_birthdays(address_book, days=7):
    try:
        days = int(days)
        return address_book.get_upcoming_birthdays(days_prior=days)
    except Exception as e:
        ErrorView(str(e)).output()
        raise ValueError("Wrong format! Command is birthdays [days_forward] (parameter is optional, default is 7 days)")

def stop_bot():
    exit(0)

def print_help():
    InfoView("""
"all" - prints all Contacts and Notes
"all-contacts" - prints all Contacts
"all-notes" - prints all Notes
"search-contacts <query string> [field:<FieldName>] [sort:<FieldName>[:direction]]" - performs search in Contacts
"search-notes <query string> [field:FieldName] [sort:FieldName[:direction]]" - performs search in Notes
"add-contact <Name>" - creates new Contact initialized with Name field
"add-note <Title>" - creates new Note initialized with Title field
"edit-contact <Name> [field:FieldName]" - searches for Contact by Name and starts fields edit procedure
"edit-note <Title> [field:FieldName]" - searches for Note by Title and starts fields edit procedure
"delete-contact <Name>" - deletes Contact found by Name
"delete-note <Title>" - deletes Note found by Title
"show-birthdays <days>" - shows Contacts whose Birthdays are happening in the closest "days" in the future
"close", "exit", "quit", "stop", "Ctrl+C", "Ctrl+D" - saves current Contacts/Notes and stops the Bot
"hello" - prints greeting message
"help" - prints this message
""").output()

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

def replace_phones_on_a_contact(record, allow_skip=False):
    existing_phones = record.phones.copy()
    new_phones = []
    populate_field(record.phones, lambda phone: new_phones.append(phone), "Enter new phone numbers (separated by space) (or 'n' to skip): ", allow_skip)

    if new_phones:
        record.phones = [Phone(phone) for phone in new_phones]
    elif not new_phones and record.phones:
        record.phones = existing_phones

#
# Parsing and running
#

command_signatures = {
    "all": [[], []],
    "all-contacts": [[], []],
    "all-notes": [[], []],
    "search-contacts": [["query"], ["field", "sort"]],
    "search-notes": [["query"], ["field", "sort"]],
    "add-contact": [["Name"], []],
    "add-note": [["Title"], []],
    "edit-contact": [["Name"], ["field"]],
    "edit-note": [["Title"], ["field"]],
    "delete-contact": [["Name"], []],
    "delete-note": [["Title"], []],
    "show-birthdays": [["days"], []],
    "close": [[], []],
    "exit": [[], []],
    "quit": [[], []],
    "stop": [[], []],
    "hello": [[], []],
    "help": [[], []]
}

class CommandsCompleter(object):
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [s for s in self.options if s and s.startswith(text)]
            else:
                self.matches = self.options[:]

        try:
            if readline.get_begidx() > 0:
                response = None
            else:
                response = self.matches[state]
        except IndexError:
            response = None

        return response

def init_autocomplete():
    readline.set_completer(CommandsCompleter([f"{cmd} " for cmd in command_signatures.keys()]).complete)
    readline.set_completer_delims(" ")
    readline.parse_and_bind('tab: complete')

def parse_command(user_input: str) -> dict|None:
    try:
        command, *args = shlex.split(user_input.strip())
    except ValueError:
        return None
    command = command.lower()

    if not command in command_signatures.keys():
        ErrorView(f"'{command}' is not a valid command.").output()
        return None

    args = list(filter(lambda a : a, [arg.strip() for arg in args]))

    required_params, _optional_params = command_signatures[command]

    required_args = args.copy()
    optional_args = {}

    args_to_remove = []
    for arg in args:
        if arg.startswith("sort:"):
            split_arg = list(filter(lambda a: a, arg.split(":")[1:3]))
            if len(split_arg) < 1:
                ErrorView(f"'{arg}' is not valid sorting parameter. Correct format is sort:FieldName[:direction]").output()
                return None
            elif len(split_arg) == 1:
                field = split_arg[0]
                sort_dir = "asc"
            else:
                field, sort_dir = split_arg
            if not field in ["Name", "Email", "Address", "Birthday", "Title", "Body"]:
                ErrorView(f"Cannot sort by '{field}' field").output()
                return None
            if not (sort_dir and sort_dir.lower() in ["asc", "desc"]):
                WarningView(f"'{sort_dir}' is not valid sorting direction. Using 'asc' instead").output()
                sort_dir = "asc"
            optional_args["sort"] = { "field": field, "direction": sort_dir }
            args_to_remove.append(arg)
        elif arg.startswith("field:"):
            try:
                field = arg.split(":")[1]
            except:
                ErrorView(f"'{arg}' is not valid field parameter. Correct format is field:FieldName").output()
                return None
            if not field in ["Name", "Phone", "Email", "Address", "Birthday", "Title", "Body", "Tags"]:
                ErrorView(f"'{field}' is not valid field").output()
                return None
            optional_args["field"] = field
            args_to_remove.append(arg)

    for arg in args_to_remove:
        required_args.remove(arg)

    if required_args and (set(required_params) & set(["Name", "Title", "query"])):
        required_args = [" ".join(required_args)]

    if len(required_args) != len(required_params):
        ErrorView(f"Check required params are present: {", ".join(required_params)}.").output()
        return None

    return {
        "command": command,
        "arguments": dict(zip(required_params, required_args)) | optional_args
    }

def run_command(user_input: str, address_book, notes_book):
    command_mappings = {
        "all": { "func": show_all, "args": [[address_book, notes_book]] },
        "all-contacts": { "func": show_all, "args": [[address_book]] },
        "all-notes": { "func": show_all, "args": [[notes_book]] },
        "search-contacts": { "func": search, "args": [address_book, "query", "field", "sort"] },
        "search-notes": { "func": search, "args": [notes_book, "query", "field", "sort"] },
        "add-contact": { "func": add_contact, "args": [address_book, "Name"] },
        "add-note": { "func": add_note, "args": [notes_book, "Title"] },
        "edit-contact": { "func": edit_contact, "args": [address_book, "Name", "field"] },
        "edit-note": { "func": edit_note, "args": [notes_book, "Title", "field"] },
        "delete-contact": { "func": delete_contact, "args": [address_book, "Name"] },
        "delete-note": { "func": delete_note, "args": [notes_book, "Title"] },
        "show-birthdays": { "func": show_birthdays, "args": [address_book, "days"] },
        "close": { "func": stop_bot, "args": [] },
        "exit": { "func": stop_bot, "args": [] },
        "quit": { "func": stop_bot, "args": [] },
        "stop": { "func": stop_bot, "args": [] },
        "hello": { "func": print, "args": ["How can I help you?"]},
        "help": { "func": print_help, "args": []}
    }

    parsed_command = parse_command(user_input)
    if not parsed_command:
        return None
    mapped_command = command_mappings[parsed_command["command"]]
    if not mapped_command:
        return None
    func_args = [parsed_command["arguments"].get(str(item), item) for item in mapped_command["args"]]
    func_args = [None if arg in ["field", "sort"] else arg for arg in func_args]

    return mapped_command["func"](*func_args)
