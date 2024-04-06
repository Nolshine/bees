from typing import Tuple

from math import sqrt

import pygame.rect

class Creature:
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = (x, y)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy
        self.area.x, self.area.y = (self.x-2, self.y-2)

    def distance_to_point(self, x: int, y: int) -> float: 
        dx, dy = self.vector_to_point(x, y)
        return sqrt(dx**2 + dy**2)
    
    def vector_to_point(self, x: int, y: int) -> Tuple[float, float]:
        dx = float(x - self.x)
        dy = float(y - self.y)
        return (dx, dy)
    
    def update(self) -> None:
        raise NotImplementedError()

class Bee(Creature):
    def __init__(self, x: int, y: int, dest: Tuple[int, int]) -> None:
        super().__init__(x, y)
        self.sprite = "bee"
        self.area = pygame.Rect(self.x-2, self.y-2, 4, 4)
        self.nectar = 0
        self.velocity = 0.0
        self.dest = dest

    def move_to_destination(self):
        dx, dy = self.vector_to_point(*self.dest)
        dist = self.distance_to_point(*self.dest)
        dx /= dist
        dy /= dist
        dx *= self.velocity
        dy *= self.velocity
        self.move(dx, dy)

    def update(self):
        if self.x != self.dest[0] and self.y != self.dest[1]:
            if self.velocity < 2:
                self.velocity += 0.01
            self.move_to_destination()

