from collections import UserDict
from datetime import date, timedelta
from typing import NamedTuple, List

from record import Record

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

    def get_upcoming_birthdays(self) -> list:
        """
        Returns a list of upcoming birthdays (celebration days).
        Returns:
            list: A list of dictionaries with names and celebration dates.
        """
        celebration_list = []
        current_date = date.today()
        for name, record in self.data.items():
            # Birthday is an optional field. Skip if it's empty
            if record.birthday is None:
                continue

            # prepare comparison data
            birthday_this_year = record.birthday.value.replace(year=date.today().year).date()

            # if the birthday has already happened, we'll celebrate next year
            if birthday_this_year < current_date:
                continue

            # if the birthday is on weekend, shift the celebration to the next Monday
            birthday_week_day = birthday_this_year.weekday()
            if birthday_week_day >= 5:
                birthady_date_this_year = birthday_this_year + timedelta(days=7 - birthday_week_day)
            else:
                birthady_date_this_year = birthday_this_year

            celebration_list.append({
                "name": name,
                "celebration_date": birthady_date_this_year})

        return celebration_list

    def search_contacts(self, keyword: str, sort: str = "", direction_text: str = "asc") -> List[Record]:
        records = [record for record in self.data.values() if record.match(keyword)]
        direction = True if direction_text == "asc" else False

        match sort:
            case "name":
                return sorted(records, key=lambda record: record.name.value, reverse=direction)
            case "phone":
                return sorted(records, key=lambda record: "".join(phone.value for phone in record.phones), reverse=direction)
            case "birthday":
                return sorted(records, key=lambda record: record.birthday.value, reverse=direction)
            case _:
                return records

