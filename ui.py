from typing import Optional, Callable

from pygame import Rect

class Button:
    def __init__(self, area: Rect, text: str, function: Optional[Callable] = None) -> None:
        self.area = area
        self.text = text
        if (function):
            self.function = function