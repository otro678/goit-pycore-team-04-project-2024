from collections import UserList
from note import Note
from views.NotesBookView import NotesBookView
from views.View import View, Sort


class Notebook(UserList):

    def __str__(self) -> str:
        return "\n".join([str(note) for note in self.data])

    def add_note(self, note: Note):
        if len(note.title) == 0 and len(note.body) == 0:
            raise ValueError("Can't add entirely empty notes")
        if self.get_note_by_title(note.title) is not None:
            raise ValueError("Note with this title already exists")
        self.data.append(note)

    def remove_note(self, title: str):
        note = self.get_note_by_title(title)
        if note is None:
            raise ValueError("Note with this title doesn't exist")
        self.data.remove(note)

    def get_notes(self) -> list:
        return self.data

    def get_note_by_title(self, title: str) -> Note:
        return next((note for note in self.data if note.title == title), None)

    @staticmethod
    def update_note(note_base: Note, new_note: Note):
        """
        Updates a left note with non-empty fields of a right note.
        Parameters:
            note_base (Note): A Note to update
            new_note (Note): A Note with fields to update
        """
        if len(new_note.title) > 0:
            note_base.title = new_note.title
        if len(new_note.body) > 0:
            note_base.body = new_note.body
        if len(new_note.tags) > 0:
            note_base.tags = new_note.tags

    def search_notes(self, keyword: str, sort: str = "", direction_text: str = "asc") -> None:
        records = [record for record in self.data if record.match(keyword)]
        direction = False if direction_text == "asc" else True

        match sort:
            case "title":
                records = sorted(records, key=lambda record: record.title, reverse=direction)
            case "body":
                records = sorted(records, key=lambda record: record.body, reverse=direction)
            case "tags":
                records = sorted(records, key=lambda record: "".join(tag for tag in record.tags), reverse=direction)
            case _:
                pass

        view = NotesBookView(records)
        view.output(sort_column=Sort(column=sort, order=direction_text), keyword=keyword)

