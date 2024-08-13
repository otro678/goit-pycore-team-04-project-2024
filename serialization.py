import pickle
from address_book import AddressBook


def save_data(book, filename="addressbook.pkl"):
    """
    Saves an address book to a pickle file.
    Parameters:
        book (AddressBook): The address book to save.
        filename (str): The name of the pickle file to save to.
    """
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    """
    Loads an address book from a pickle file, or creates a new one if the file does not exist.
    Parameters:
        filename (str): The name of the pickle file to load.
    Returns:
        AddressBook: The loaded or newly created address book.
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено