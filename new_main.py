import sys
from serialization import save_data, load_contacts, load_notes
from views.TextView import ErrorView, InfoView
from commands import *

def main():
    if sys.version_info[0:2] != (3, 12):
        ErrorView('Sorry, app requires Python 3.12, please consult with a Readme file about the setup instructions').output()
        sys.exit(1)

    address_book = load_contacts()
    notes_book = load_notes()
    InfoView("Welcome to the assistant bot!").output()

    try:
        while True:
            print(run_command(input("Enter command: "), address_book, notes_book))
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        save_data(address_book)
        save_data(notes_book, filename="notes.pkl")
        InfoView("Good bye!").output()

if __name__ == "__main__":
    main()
