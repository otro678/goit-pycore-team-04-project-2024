from typing import List

from record import Record
from views.View import View

class AddressBookView(View):
    data: List[Record]

    def __init__(self, contact_list: List[Record]):
        # possible validation of type
        super().__init__(contact_list)
        self.header = ['Name', 'Phone', 'Address', 'Birthday', 'Email']
        self.title = "Addressbook view"

    def get_row(self, record: Record, keyword: str):
        return [
            self.escape(record.name.value, keyword),
            self.escape(", ".join(phone.value for phone in record.phones), keyword),
            self.escape(record.address.value, keyword),
            self.escape(str(record.birthday.value), keyword),
            self.escape(record.email.value, keyword),
        ]
