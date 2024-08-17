from typing import List

from note import Note, NOTES_BOOK_FIELDS
from views.TableView import TableView
from views.View import OutputData


class NotesBookView(TableView):
    data: List[Note]

    def __init__(self, contact_list: List[Note]):
        # possible validation of type
        super().__init__(contact_list)
        self.output_data = OutputData()
        self.header = [NOTES_BOOK_FIELDS.TITLE.value, NOTES_BOOK_FIELDS.BODY.value, NOTES_BOOK_FIELDS.TAGS.value]
        self.title = "Notes book view"

    def get_row(self, record: Note):
        return [
            self.escape(record.title),
            self.escape(record.body),
            self.escape(", ".join(tag for tag in record.tags)),
        ]
