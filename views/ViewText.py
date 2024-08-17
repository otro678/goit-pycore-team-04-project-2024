from enum import Enum

from views.View import View

class TextType(Enum):
    ERROR = 1,
    WARNING = 2,
    INFO = 3

class ViewText(View):
    pass