from collections import UserList
from typing import List

from note import Note, NOTES_BOOK_FIELDS
from views.TableView import TableView, Sort
from views.NotesBookView import NotesBookView

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

    def search(self, keyword: str, field: NOTES_BOOK_FIELDS = NOTES_BOOK_FIELDS.ALL, sort: NOTES_BOOK_FIELDS = NOTES_BOOK_FIELDS.EMPTY, direction_text: str = "asc") -> None:
        if field not in NOTES_BOOK_FIELDS or sort not in NOTES_BOOK_FIELDS:
            raise KeyError(f"Field {field} not found.")

        notes = self.__filter(keyword, field)
        notes = self.__sort(notes, field, direction_text)

        view = NotesBookView(notes)
        view.sort_column = Sort(column=sort, order=direction_text)
        view.keyword = keyword
        view.output()

    def __filter(self, keyword: str, field: NOTES_BOOK_FIELDS) -> List[Note]:
        notes = self.data
        match field:
            case NOTES_BOOK_FIELDS.ALL:
                notes = [note for note in notes if note.match(keyword)]
            case NOTES_BOOK_FIELDS.TAGS:
                notes = [note for note in notes if any([tag.lower().find(keyword.lower()) >= 0 for tag in note.tags])]
            case NOTES_BOOK_FIELDS.BODY:
                notes = [note for note in notes if note.body.lower().find(keyword.lower()) >= 0]
            case NOTES_BOOK_FIELDS.TITLE:
                notes = [note for note in notes if note.title.lower().find(keyword.lower()) >= 0]

        return notes

    def __sort(self, notes: List[Note], field: NOTES_BOOK_FIELDS, direction_text: str) -> List[Note]:
        direction = False if direction_text == "asc" else True

        match field:
            case NOTES_BOOK_FIELDS.TAGS:
                notes = sorted(notes, key=lambda note: "".join(tag for tag in note.tags), reverse=direction)
            case NOTES_BOOK_FIELDS.BODY:
                notes = sorted(notes, key=lambda note: note.body, reverse=direction)
            case NOTES_BOOK_FIELDS.TITLE:
                notes = sorted(notes, key=lambda note: note.title, reverse=direction)
            case _:
                pass

        return notes
