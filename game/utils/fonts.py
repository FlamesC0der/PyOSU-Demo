import pygame

from game.resources.colors import *
from game.utils.image_loader import load_image


def render_text(surface, text: str, size: int, position: tuple):
    font = pygame.font.Font(None, size)
    text_render = font.render(text, True, white)
    surface.blit(text_render, position)


def render_number(surface, number_str: str, position: tuple):
    number_images = [load_image(f"skins/score-{i}.png") for i in range(10)]
    comma_image = load_image('skins/score-comma.png')
    dot_image = load_image('skins/score-dot.png')
    percent_image = load_image('skins/score-percent.png')

    for i, char in enumerate(number_str):
        if char.isdigit():
            digit_image = number_images[int(char)]
        elif char == ',':
            digit_image = dot_image
        elif char == '.':
            digit_image = dot_image
        elif char == '%':
            digit_image = percent_image
        else:
            continue

        digit_width = digit_image.get_width()

        surface.blit(digit_image, (position[0] + i * digit_width, position[1]))
