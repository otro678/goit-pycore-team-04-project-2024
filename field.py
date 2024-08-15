import re
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def match(self, value, strict=False):
        if strict:
            return self.value == value

        return type(self.value) is str and self.value.lower().find(value.lower()) >= 0


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(self.validated_phone(value))

    def validated_phone(self, phone: str) -> str:
        if not len(phone) == 10 and phone.isdigit():
            raise ValueError("Invalid phone number: {phone}. Must be 10-digits long.")
        return phone


class Birthday(Field):
    def __init__(self, value: str):
        self.value = self.validate_birthday(value)
        
    def validate_birthday(self, value: str):
        formats = ["%d.%m.%Y", "%d %m %Y","%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]
        birth_date = None
        for format in formats:
            try:
                birth_date = datetime.strptime(value, format)
                break
            except ValueError:
                continue
        if not birth_date:
            raise ValueError("Invalid date format. Try DD.MM.YYYY")
        if (datetime.now() - birth_date).days / 365 > 115:
            raise ValueError("Year of birth seems to be incorrect. Or you might be not alive already.")
        return birth_date
            
    def match(self, value, strict=False):
        # TODO: let's discuss tomorrow if we're going to search by date
        return False

class Email(Field):
    def __init__(self, value):
        self.value = self.validate_email(value)

    def validate_email(self, email: str) -> str:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError(f"Invalid format of email: {email}.")
        return email


class Address(Field):
    pass