from __future__ import annotations

from typing import Iterable, TYPE_CHECKING

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE

from globals import *
from image_manager import ImageManager
from ui import Button

if TYPE_CHECKING:
    from creatures import Creature
    from buildings import Building


class Engine:
    def __init__(
            self,
            screen: pygame.Surface,
            game_bg: pygame.Surface,
            game_fg: pygame.Surface,
            menu_bar: pygame.Surface,
            image_manager: ImageManager,
            creatures: Iterable[Creature] = [],
            buildings: Iterable[Building] = [],
            buttons: Iterable[Button] = [],
    ) -> None:
        self.screen = screen
        self.game_bg = game_bg
        self.game_fg = game_fg
        self.menu_bar = menu_bar
        self.image_manager = image_manager
        self.creatures = creatures
        self.buildings = buildings
        self.buttons = buttons

    def render_all(self) -> None:
        self.game_fg.blit(self.game_bg, (0, 0))
        for building in self.buildings:
            self.game_fg.blit(
                self.image_manager.use(building.sprite), building.area
            )
        for creature in self.creatures:
            self.game_fg.blit(
                self.image_manager.use(creature.sprite), creature.area
            )

        self.screen.blit(self.game_fg, (0, 0))
        self.menu_bar.fill((0, 0, 0))
        for button in self.buttons:
            self.render_button(button)
        self.screen.blit(self.menu_bar, (0, GAME_AREA[1]))

    def render_button(self, button: Button) -> None:
        # check for mouseover, use appropriate image
        # Absolute position
        mouse_pos = pygame.mouse.get_pos()
        # position relative to top of menu bar
        rel_pos = (mouse_pos[0], mouse_pos[1]-GAME_AREA[1])
        if button.area.collidepoint(rel_pos):
            image = self.image_manager.use("button_hl")
        else:
            image = self.image_manager.use("button")
        image = pygame.transform.smoothscale(
            image, (button.area.width, button.area.height)
        )
        self.menu_bar.blit(image, button.area)

        # rendering text
        font = pygame.font.Font(None, 22)
        text = font.render(button.text, False, (0, 0, 0))
        textpos = text.get_rect()
        textpos.center = button.area.center
        self.menu_bar.blit(text, textpos)

    def render_background(self, worldmap: Iterable[Iterable[float]]) -> None:
        for col in range(WORLD_WIDTH):
            for row in range(WORLD_HEIGHT):
                if worldmap[row][col] > 0:
                    image = self.image_manager.use("grass")
                else:
                    image = self.image_manager.use("dirt")
                self.game_bg.blit(image, (col*TILE_SIZE, row*TILE_SIZE))

    def update_creatures(self) -> None:
        for creature in self.creatures:
            creature.update()

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if (
                (event.type == KEYDOWN and event.key == K_ESCAPE)
                or event.type == QUIT
            ):
                return False
        return True
        
