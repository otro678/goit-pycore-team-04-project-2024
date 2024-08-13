from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.value = self.validated_phone(value)

    def validated_phone(self, phone: str) -> str:
        if not len(phone) == 10 and phone.isdigit():
            raise ValueError("Invalid phone number: {phone}. Must be 10-digits long.")
        return phone


class Birthday(Field):
    def __init__(self, value: str):
        try:
            # TODO Add multiple bday formats & max age check
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Email(Field):
    def __init__(self, value):
        self.value = self.validate_email(value)

    def validate_email(self, email: str) -> str:
        # TODO Replace with a correct check
        if "@" not in email or "." not in email:
            raise ValueError(f"Invalid email: {email}.")
        return email


class Address(Field):
    pass