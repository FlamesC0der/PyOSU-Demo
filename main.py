import sys
import pygame
import pygame_gui

from game.resources.colors import *
from game.utils.image_loader import load_image
from level import play_level
from log import logger

pygame.init()
pygame.mixer.init()

logger.info("PyOSU by FlamesCoder")

screen_info = pygame.display.Info()
size = width, height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("PyOSU")

ui_manager = pygame_gui.UIManager(size)

all_sprites = pygame.sprite.Group()

EXIT_INTRO = pygame.USEREVENT + 1


class Intro(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('game/resources/textures/FS_logo.png')
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect()

        self.rect.centerx = width // 2
        self.rect.centery = height // 2

        self.status = 0
        self.alpha = 0

    def update(self, *args):
        if self.status == 0:
            self.alpha += 1
        elif self.status == 1:
            self.alpha -= 0.5

        if self.status == 0 and self.alpha >= 255:
            self.status = 1
            self.alpha = 500
        if self.status == 1 and self.alpha <= 0:
            self.kill()
            pygame.event.post(pygame.event.Event(EXIT_INTRO))
        self.image.set_alpha(self.alpha)


Intro(all_sprites)

running = True

# Intro
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == EXIT_INTRO:
            running = False

    screen.fill(black)

    all_sprites.draw(screen)
    all_sprites.update()

    pygame.display.flip()

running = True

# Main Menu
# bg = load_image('game/resources/bgs/main_menu.jpeg')
# bg = pygame.transform.scale(bg, size)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(black)
    # screen.blit(bg, (0, 0))

    pygame.display.flip()

    key = pygame.key.get_pressed()

    if key[pygame.K_1]:
        score, accuracy = play_level(screen, ui_manager, size, "Classroom_of_the_elite_Hito_Jibai")
    if key[pygame.K_2]:
        score, accuracy = play_level(screen, ui_manager, size, "Airi Suzuki - Heart wa Oteage (TV Size)")
