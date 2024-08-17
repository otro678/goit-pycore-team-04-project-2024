from collections import UserDict
from datetime import date, timedelta
from typing import List

from field import Date, Name, Address, Email, Birthday
from record import Record, ADDRESS_BOOK_FIELDS
from views.TableView import Sort
from views.AddressBookView import AddressBookView

class AddressBook(UserDict):

    """
    A simple address book implementation that stores records in a dictionary.
    """
    def __str__(self) -> str:
        return "\n".join([str(record) for record in self.data.values()])

    def add_record(self, record: Record):
        """
        Adds a record to the address book.
        Parameters:
            record (Record): The record to add.
        Raises:
            KeyError: If a record with the same name already exists.
        """
        if record.name.value in self.data:
            raise KeyError(f"A record with name {record.name.value} already exists.")
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """
        Finds a record by name.
        Parameters:
            name (str): The name of the record to find.
        Returns:
            Record: The record with the given name, or None if not found.
        """
        return self.data.get(name)

    def delete(self, name: str):
        """
        Deletes a record by name.
        Parameters:
            name (str): The name of the record to delete.
        Raises:
            KeyError: If no record with the given name is found.
        """
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"A record with name {name} not found.")

    def get_upcoming_birthdays(self, days_prior: int = 7) -> None:
        """
        Returns a list of upcoming birthdays (celebration days).
        Parameters:
            days_prior (int, optional): The number of days in the future to look for birthdays.
                Defaults to 7.
        Returns:
            list: A list of dictionaries with names and celebration dates.
        """
        celebration_list = []
        current_date = date.today()
        celebration_period = current_date + timedelta(days=days_prior)
        for name, record in self.data.items():
            # Birthday is an optional field. Skip if it's empty
            if record.birthday is None:
                continue

            # prepare comparison data
            celebration_date = record.birthday.value.replace(year=date.today().year).date()

            # if the birthday has already happened, we'll celebrate next year
            if celebration_date < current_date:
                celebration_date = celebration_date.replace(year=celebration_date.year + 1)

            # if the birthday is on weekend, shift the celebration to the next Monday
            celebration_week_day = celebration_date.weekday()
            if celebration_week_day >= 5:
                celebration_date = celebration_date + timedelta(days=7 - celebration_week_day)

            # if the celebration date fits the celebration period, add it to the list
            if celebration_date <= celebration_period:
                celebration_list.append(record)


        view = AddressBookView(celebration_list)
        view.sort_column = Sort(column=ADDRESS_BOOK_FIELDS.BIRTHDAY, order="asc")
        view.output()

    def search_by_date(self, from_date: Date, to_date: Date) -> None:
        records = [record for record in self.data.values() if record.birthday.is_between(from_date=from_date, to_date=to_date)]
        view = AddressBookView(records)
        view.sort_column = Sort(column=ADDRESS_BOOK_FIELDS.BIRTHDAY, order="asc")
        view.output()

    def search(self, keyword: str, field: ADDRESS_BOOK_FIELDS = ADDRESS_BOOK_FIELDS.ALL, sort: ADDRESS_BOOK_FIELDS = ADDRESS_BOOK_FIELDS.EMPTY, direction_text: str = "asc") -> None:
        if field not in ADDRESS_BOOK_FIELDS or sort not in ADDRESS_BOOK_FIELDS:
            raise KeyError(f"Field {field} not found.")

        records = self.__filter(keyword, field)
        records = self.__sort(records, field, direction_text)

        view = AddressBookView(records)
        view.sort_column=Sort(column=sort, order=direction_text)
        view.keyword=keyword
        view.output()

    def __filter(self, keyword: str, field: ADDRESS_BOOK_FIELDS):
        records = self.data.values()
        match field:
            case ADDRESS_BOOK_FIELDS.ALL:
                records = [record for record in records if record.match(keyword)]
            case ADDRESS_BOOK_FIELDS.NAME:
                records = [record for record in records if isinstance(record.name, Name) and record.name.match(keyword)]
            case ADDRESS_BOOK_FIELDS.ADDRESS:
                records = [record for record in records if isinstance(record.address, Address) and record.address.match(keyword)]
            case ADDRESS_BOOK_FIELDS.EMAIL:
                records = [record for record in records if isinstance(record.email, Email) and record.email.match(keyword)]
            case ADDRESS_BOOK_FIELDS.EMAIL:
                records = [record for record in records if record.match_phone(keyword)]

        return records

    def __sort(self, records: List[Record], field: ADDRESS_BOOK_FIELDS, direction_text: str):
        direction = False if direction_text == "asc" else True

        match field:
            case ADDRESS_BOOK_FIELDS.NAME:
                records = sorted(records, key=lambda record: record.name.value if isinstance(record.name, Name) else "", reverse=direction)
            case ADDRESS_BOOK_FIELDS.ADDRESS:
                records = sorted(records, key=lambda record: record.address.value if isinstance(record.address, Address) else "", reverse=direction)
            case ADDRESS_BOOK_FIELDS.EMAIL:
                records = sorted(records, key=lambda record: record.email.value if isinstance(record.email, Email) else "", reverse=direction)
            case ADDRESS_BOOK_FIELDS.PHONE:
                records = sorted(records, key=lambda record: "".join(phone.value for phone in record.phones), reverse=direction)
            case ADDRESS_BOOK_FIELDS.BIRTHDAY:
                records = sorted(records, key=lambda record: record.birthday.value if isinstance(record.birthday, Birthday) else "", reverse=direction)
            case _:
                pass

        return records
