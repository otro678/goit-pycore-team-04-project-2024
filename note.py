from enum import Enum


class NOTES_BOOK_FIELDS(str, Enum):
    EMPTY = "",
    ALL = "all",
    TITLE = "title",
    BODY = "body",
    TAGS = "tags",


class Note:
    def __init__(self, title: str = "", body: str = ""):
        self.__title = title
        self.__body = body
        self.__tags = []

    def __str__(self):
        return f"Title: {self.__title}, Body: {self.__body}, Tags: {','.join(self.__tags)}"

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, new_title: str):
        self.__title = new_title

    @property
    def body(self) -> str:
        return self.__body

    @body.setter
    def body(self, new_body: str):
        self.__body = new_body

    @property
    def tags(self) -> list:
        return self.__tags

    @tags.setter
    def tags(self, new_tags: list):
        self.__tags = new_tags

    def match(self, keyword: str) -> bool:
        return (self.__title.lower().find(keyword.lower()) >= 0
                or self.__body.lower().find(keyword.lower()) >= 0
                or any([tag.lower().find(keyword.lower()) >= 0 for tag in self.tags]))
