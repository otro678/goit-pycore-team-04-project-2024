from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def match(self, value, strict=False):
        if strict:
            return self.value == value

        return self.value.lower().find(value.lower()) >= 0


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
        try:
            super().__init__(datetime.strptime(value, "%d.%m.%Y"))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
