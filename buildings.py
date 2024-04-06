from random import randint

import pygame.rect

from globals import TILE_SIZE

class Building:
    def __init__(
            self,
            tilex: int,
            tiley: int,
            area: pygame.Rect,
            sprite: str,
        ) -> None:
        self.x = tilex
        self.y = tiley
        self.area = area
        self.sprite = sprite

class Hive(Building):
    def __init__(
            self,
            tilex: int,
            tiley: int,
        ) -> None:
        global TILE_SIZE
        area = pygame.Rect(
            tilex*TILE_SIZE,
            tiley*TILE_SIZE,
            2 * TILE_SIZE,
            2 * TILE_SIZE,
        )
        sprite = "hive"
        super().__init__(tilex, tiley, area, sprite)

class Flower(Building):
    def __init__(
            self,
            tilex: int,
            tiley: int,
        ) -> None:
        global TILE_SIZE
        area = pygame.Rect(
            tilex * TILE_SIZE,
            tiley * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE,
        )
        sprite = "flower"
        super().__init__(tilex, tiley, area, sprite)
        self.nectar = randint(1, 15)

    def take_nectar(self, value: int) -> int:
        if value > self.nectar:
            value = self.nectar
        self.nectar -= value
        return value