class Note:
    def __init__(self, title: str = "", body: str = ""):
        self.__title = title
        self.__body = body

    def __str__(self):
        return f"{self.__title}: {self.__body}"

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
