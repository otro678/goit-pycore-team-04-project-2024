from collections import UserList
from note import Note


class Notebook(UserList):

    def __str__(self) -> str:
        return "\n".join([str(note) for note in self.data])

    def add_note(self, note: Note):
        if len(note.title) == 0 and len(note.body) == 0:
            raise ValueError("Can't add entirely empty notes")
        if self.get_note_by_title(note.title) is not None:
            raise ValueError("Note with this title already exists")
        self.data.append(note)

    def get_notes(self) -> list:
        return self.data

    def get_note_by_title(self, title: str) -> Note:
        for note in self.data:
            if note.title == title:
                return note
        return None

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
