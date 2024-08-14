from typing import List

from field import Name, Phone, Birthday

class Record:
    def __init__(self, name):
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Birthday | None = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str):
        if not any(p.value == phone for p in self.phones):
            self.phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def remove_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Phone number {phone} not found in record.")

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def match_phone(self, phone: str) -> bool:
        return any([record.match(phone) for record in self.phones])

    def match(self, keyword: str) -> bool:
        return (self.name.match(keyword)
                or self.match_phone(keyword)
                or self.birthday.match(keyword))