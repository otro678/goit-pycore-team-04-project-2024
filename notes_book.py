from collections import UserList
from note import Note


class Notebook(UserList):

    def __str__(self) -> str:
        return "\n".join([str(note) for note in self.data])

    def add_note(self, note: Note):
        self.data.append(note)
