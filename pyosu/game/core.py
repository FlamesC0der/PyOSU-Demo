import pygame
import asyncio

from pyosu.game.utils.image_loader import load_image


class Cursor(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()

        self.image = load_image("skins/cursor.png")
        self.rect = self.image.get_rect()

        self.screen = screen

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen.blit(self.image, self.rect)


def cursor_change(cursor):
    while True:
        cursor.update()
