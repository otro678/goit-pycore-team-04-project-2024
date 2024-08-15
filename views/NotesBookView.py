from typing import List

from note import Note
from views.View import View

class NotesBookView(View):
    data: List[Note]

    def __init__(self, contact_list: List[Note]):
        # possible validation of type
        super().__init__(contact_list)
        self.header = ['Title', 'Body', 'Tags']
        self.title = "Notes book view"

    def get_row(self, record: Note, keyword: str):
        return [
            self.escape(record.title, keyword),
            self.escape(record.body, keyword),
            self.escape(", ".join(tag for tag in record.tags), keyword),
        ]
