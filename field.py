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
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(self.validated_phone(value))

    def validated_phone(self, phone: str) -> str:
        pattern = r"^(\(?\d{3}\)?[-]?\d{2,3}[-]?\d{2}[-]?\d{2,4}|\d{10})$"
        if not re.match(pattern, phone):
            raise ValueError(f"Invalid phone number: {phone}.")
        
        clean_phone = re.sub(r'\D', '', phone)

        if len(clean_phone) != 10:
            raise ValueError(f"Invalid phone number: {phone}. It should contain exactly 10 digits.")

        return clean_phone

class Date(Field):
    def __init__(self, value: str):
        super().__init__(self.validate_date(value))

    def validate_date(self, value: str) -> datetime:
        formats = ["%d.%m.%Y", "%d %m %Y","%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]
        birth_date = None
        for date_format in formats:
            try:
                birth_date = datetime.strptime(value, date_format)
                break
            except ValueError:
                continue
        if not birth_date:
            raise ValueError("Invalid date format. Try DD.MM.YYYY")

        return birth_date


class Birthday(Date):
    def __init__(self, value: str):
        self.value = self.validate_birthday(value)

    def validate_birthday(self, value: str):
        birth_date = self.validate_date(value)
        if (datetime.now() - birth_date).days / 365 > 115:
            raise ValueError("Year of birth seems to be incorrect. Or you might be not alive already.")
        if datetime.now() < birth_date:
            raise ValueError("Year of birth seems to be incorrect. Or you are not born yet.")
        return birth_date

    def is_between(self, from_date: Date | None, to_date: Date | None) -> bool:
        res = from_date is None or self.value >= from_date.value
        res &= to_date is None or self.value <= to_date.value
        return res

    def match(self, value, strict=False):
        # TODO: let's discuss tomorrow if we're going to search by date
        return False

class Email(Field):
    def __init__(self, value):
        super().__init__(self.validate_email(value))

    def validate_email(self, email: str) -> str:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError(f"Invalid format of email: {email}.")
        return email


class Address(Field):
    def __init__(self, value):
        super().__init__(value)