from typing import Iterable

import pygame.image
import pygame.surface

class ImageManager:
    def __init__(self) -> None:
        self.images = {}

    def load(self, name: str, image: str) -> pygame.surface.Surface:
        if not (image in self.images):
            self.images[name] = pygame.image.load(image)# .convert()
            return self.images[name]
        else:
            return self.images[name]
        
    def use(self, name: str) -> pygame.surface.Surface:
        return self.images[name]

    def load_from_names(self, names: Iterable[str]) -> None:
        for name in names:
            self.load(name, f"{name}.png")