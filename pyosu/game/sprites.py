import pygame

from pyosu.game.utils.image_loader import load_image
from pyosu.game.utils.fonts import render_number


class Rating_image(pygame.sprite.Sprite):
    def __init__(self, *groups, rating_type, x, y):
        super().__init__(*groups)

        self.image = load_image(f"skins/ranking-{rating_type}.png")
        self.image = pygame.transform.scale(self.image, (600, 600))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.centery = y


class Result_types(pygame.sprite.Sprite):
    def __init__(self, *groups, rating_type, x, y):
        super().__init__(*groups)

        if rating_type == 300:
            rating_type = f"{rating_type}g-0"

        self.image = load_image(f"skins/mania-hit{rating_type}.png")

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Back_Button(pygame.sprite.Sprite):
    def __init__(self, *groups, size):
        super().__init__(*groups)

        self.image = load_image("skins/menu-back.png")

        self.rect = self.image.get_rect()
        self.rect.x = 15
        self.rect.y = size[1] - 100
