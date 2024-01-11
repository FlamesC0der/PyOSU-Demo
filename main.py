import sys
import pygame
import pygame_gui
import os

from game.resources.colors import *
from game.utils.image_loader import load_image
from game.utils.fonts import render_text
from game.utils.level_data import load_level_data
from level import play_level
from log import logger

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()

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

bg = load_image('game/resources/textures/bg.jpeg')
bg = pygame.transform.scale(bg, size)


def get_levels():
    levels = [d for d in os.listdir('songs') if os.path.isdir(os.path.join('songs', d))]
    return levels


levels = get_levels()
selected_song = get_levels()[0]


class Song(pygame.sprite.Sprite):
    def __init__(self, *groups, name, index):
        super().__init__(*groups)

        self.image = pygame.Surface((750, 100))
        self.image.fill(black)

        self.index = index

        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.y = self.index * 110 + 10

        self.name = name
        self.selected = False
        self.logo = load_image(f'songs/{name}/bg.jpg')
        self.logo = pygame.transform.scale(self.logo, (100, 100))
        self.image.blit(self.logo, (0, 0))
        render_text(self.image, self.name, 25, (150, 45))

    def update(self):
        if self.selected:
            self.image.fill(grey)
        else:
            self.image.fill(black)
        self.image.blit(self.logo, (0, 0))
        render_text(self.image, self.name, 25, (150, 45))


for i, song in enumerate(levels):
    Song(all_sprites, name=song, index=i)

selected_song_index = 0
current_song_index = 0
current_music = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_song_index = max(0, selected_song_index - 1)
            elif event.key == pygame.K_DOWN:
                selected_song_index = min(len(levels) - 1, selected_song_index + 1)
            elif event.key == pygame.K_RETURN:
                selected_song = levels[selected_song_index]
                logger.warn(selected_song)
                # current_music.stop()
                play_level(screen, ui_manager, size, selected_song)

    screen.blit(bg, (0, 0))

    for i, song in enumerate(all_sprites.sprites()):
        if i == selected_song_index:
            song.selected = True
            bg, music, notes = load_level_data(levels[i])
            bg = pygame.transform.scale(bg, (width, height))

            # if current_song_index != selected_song_index:
            #     logger.warn(f"changed music form {current_song_index} to {selected_song_index}")
            #     current_song_index = selected_song_index
            #     if current_music:
            #         logger.warning("stoped playing")
            #         current_music.stop()
            #     current_music = music
            #     current_music.play()
            #     logger.warning("Start playing")
        else:
            song.selected = False

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
