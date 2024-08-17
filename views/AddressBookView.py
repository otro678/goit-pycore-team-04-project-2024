from typing import List

from record import Record, ADDRESS_BOOK_FIELDS
from views.ViewTable import ViewTable

class AddressBookView(ViewTable):
    data: List[Record]

    def __init__(self, contact_list: List[Record]):
        # possible validation of type
        super().__init__(contact_list)
        self.header = [
            ADDRESS_BOOK_FIELDS.NAME.value,
            ADDRESS_BOOK_FIELDS.PHONE.value,
            ADDRESS_BOOK_FIELDS.ADDRESS.value,
            ADDRESS_BOOK_FIELDS.BIRTHDAY.value,
            ADDRESS_BOOK_FIELDS.EMAIL.value]
        self.title = "Addressbook view"

    def get_row(self, record: Record):
        return [
            self.escape(record.name.value),
            self.escape(", ".join(phone.value for phone in record.phones)),
            self.escape(record.address.value),
            self.escape(str(record.birthday.value)),
            self.escape(record.email.value),
        ]
