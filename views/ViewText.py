from enum import Enum

from views.View import View

class TextType(Enum):
    ERROR = 1,
    WARNING = 2,
    INFO = 3

class ViewText(View):
    def __init__(self, text: str, text_type: TextType = TextType.INFO):
        self.output_data.data = text
        match text_type:
            case TextType.ERROR:
                self.output_data.style = "bold red"

            case TextType.WARNING:
                self.output_data.style = "bold yellow"

            case _:
                self.output_data.style = ""

