import os
import pygame


def load_image(path: str, color_key=None):
    try:
        image = pygame.image.load(path).convert()

        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        else:
            image = image.convert_alpha()
        return image
    except Exception as e:
        print("Cannot load image:", path, e)
        return None
