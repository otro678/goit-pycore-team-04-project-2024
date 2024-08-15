from collections import UserList
from note import Note


class Notebook(UserList):

    def __str__(self) -> str:
        return "\n".join([str(note) for note in self.data])

    def add_note(self, note: Note):
        if len(note.title) == 0 and len(note.body) == 0:
            raise ValueError("Can't add entirely empty notes")
        self.data.append(note)

    def get_notes(self) -> list:
        return self.data
