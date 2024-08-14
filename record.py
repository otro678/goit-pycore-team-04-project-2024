from typing import List
from field import Name, Phone, Birthday, Email, Address


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None
        self.address = None

    def __str__(self):
        phones = ', '.join(p.value for p in self.phones)
        email = self.email.value if self.email else "No email"
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "No birthday"
        address = self.address.value if self.address else "No address"
        return (f"Contact name: {self.name.value}, phones: {phones}, "
                f"email: {email}, birthday: {birthday}, address: {address}")

    def add_phone(self, phone: str):
        if not any(p.value == phone for p in self.phones):
            self.phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

    def add_email(self, email: str):
        self.email = Email(email)

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def match_phone(self, phone: str) -> bool:
        return any([record.match(phone) for record in self.phones])

    def match(self, keyword: str) -> bool:
        return (self.name.match(keyword)
                or self.match_phone(keyword)
                or self.birthday.match(keyword)
                or self.email.match(keyword)
                or self.address.match(keyword))

    def add_address(self, address: str):
        self.address = Address(address)