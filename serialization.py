import pickle
from address_book import AddressBook
from notes_book import Notebook
import os

user_folder = os.path.expanduser("~")
app_folder = os.path.join(user_folder, '.mason_app')

if not os.path.exists(app_folder):
    os.makedirs(app_folder)

def save_data(book, filename="addressbook.pkl"):
    """
    Saves an address book to a pickle file.
    Parameters:
        book (AddressBook): The address book to save.
        filename (str): The name of the pickle file to save to.
    """
    filepath = os.path.join(app_folder, filename)
    with open(filepath, "wb") as f:
        pickle.dump(book, f)


def load_contacts(filename="addressbook.pkl"):
    """
    Loads an address book from a pickle file, or creates a new one if the file does not exist.
    Parameters:
        filename (str): The name of the pickle file to load.
    Returns:
        AddressBook: The loaded or newly created address book.
    """
    filepath = os.path.join(app_folder, filename)
    try:
        with open(filepath, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def load_notes(filename="notes.pkl"):
    """
    Loads an notes book from a pickle file, or creates a new one if the file does not exist.
    Parameters:
        filename (str): The name of the pickle file to load.
    Returns:
        AddressBook: The loaded or newly created address book.
    """
    filepath = os.path.join(app_folder, filename)
    try:
        with open(filepath, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return Notebook()  # Повернення нової адресної книги, якщо файл не знайдено
