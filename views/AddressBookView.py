from typing import List

from field import Field
from record import Record, ADDRESS_BOOK_FIELDS
from views.TableView import TableView
from views.View import OutputData


class AddressBookView(TableView):
    data: List[Record]

    def __init__(self, contact_list: List[Record]):
        # possible validation of type
        super().__init__(contact_list)
        self.output_data = OutputData()
        self.header = [
            ADDRESS_BOOK_FIELDS.NAME.value,
            ADDRESS_BOOK_FIELDS.PHONE.value,
            ADDRESS_BOOK_FIELDS.ADDRESS.value,
            ADDRESS_BOOK_FIELDS.BIRTHDAY.value,
            ADDRESS_BOOK_FIELDS.EMAIL.value]
        self.title = "Addressbook view"

    def get_row(self, record: Record):
        return [
            self.escape(record.name.value if isinstance(record.name, Field) else ''),
            self.escape(", ".join(phone.value if isinstance(phone, Field) else '' for phone in record.phones)),
            self.escape(record.address.value if isinstance(record.address, Field) else ''),
            self.escape(str(record.birthday.value if isinstance(record.birthday, Field) else '')),
            self.escape(record.email.value if isinstance(record.email, Field) else ''),
        ]
