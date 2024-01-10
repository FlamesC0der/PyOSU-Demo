import sys
import os
import math
import pygame

from game.resources.colors import *
from game.utils.image_loader import load_image
from game.utils.rating import get_rating
from game.utils.fonts import render_text, render_number
from settings import key_mapping, rating
from log import logger

clock = pygame.time.Clock()


def load_level_data(name):
    music, bg, notes = None, None, []

    with open(f"songs/{name}/data.osu", "r") as f:
        general = False
        hit_objects = False
        for line in list(map(lambda s: s.strip(), f.readlines())):
            if "[General]" in line:
                general = True
            elif "[HitObjects]" in line:
                general = False
                hit_objects = True
            elif general and line:
                if "AudioFilename" in line:
                    try:
                        music = pygame.mixer.Sound(f"songs/{name}/{line.split(': ')[1]}")
                    except Exception as e:
                        logger.error("Failed to load music")
            elif hit_objects and line:
                values = line.split(",")

                time = int(values[2])
                column = int(values[0]) % 5
                note_type = int(values[3])

                notes.append({"time": time, "column": column, "type": note_type})

    try:
        bg = load_image(f"songs/{name}/bg.jpg")
    except Exception as e:
        logger.error("Failed to load bg")

    return bg, music, notes


def play_level(screen, ui_manager, size, name):
    global total_notes
    logger.info("")
    logger.info(f"Play level {name}")

    game_surface_width = 500
    game_surface = pygame.Surface((game_surface_width, size[1]))

    button_width = game_surface_width // 5
    button_height = 50

    button_positions = [(i * button_width, size[1] - 50) for i in range(5)]

    running = True

    bg, music, notes = load_level_data(name)
    logger.info("Data loaded")

    if bg:
        bg = pygame.transform.scale(bg, size)
    if music:
        music.play()

    start_time = pygame.time.get_ticks()

    logger.info("Starting level")

    # Stats
    logger.info(f"Total notes: {len(notes)}")
    score = 0
    total_notes = 0
    notes_clicked = 0
    accuracy = 0

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    note_sprites = pygame.sprite.Group()
    bottom_buttons_sprites = pygame.sprite.Group()

    # class HitImage(pygame.sprite.Sprite):
    #     def __init__(self, *groups, x, y, creation_time):
    #         super().__init__(*groups)
    #
    #         self.image = load_image("skins/mania-hit100.png", color_key=1)
    #         self.rect = self.image.get_rect()
    #         self.rect.x = x
    #         self.rect.y = y - 50
    #
    #         self.creation_time = creation_time
    #
    #     def update(self):
    #         pass
    #         # if pygame.time.get_ticks() - self.creation_time >= 1000:
    #         #     self.kill()

    class Note(pygame.sprite.Sprite):
        def __init__(self, button_width, column, start_time, note_type):
            super().__init__()

            self.image = pygame.Surface((button_width, 30))
            self.image.fill((250, 238, 105))

            self.rect = self.image.get_rect()
            self.rect.x = column * 100
            self.rect.y = 0

            self.column = column

            self.time = start_time
            self.note_type = note_type
            self.start_time = start_time - 2000
            self.height = size[1]

            self.pressed = False

        def update(self, current_time):
            global total_notes
            progress = min(1, (current_time - self.start_time) / 2000)
            self.rect.y = int(progress * self.height)

            if self.rect.y >= size[1] - 50:
                total_notes += 1
                self.kill()

    class ClickButton(pygame.sprite.Sprite):
        def __init__(self, *groups, index):
            super().__init__(*groups)

            self.image = load_image("skins/mania-key1D.png")
            self.image = pygame.transform.scale(self.image, (button_width, button_height * 2))
            self.rect = self.image.get_rect()

            self.index = index
            self.height = size[1]

            self.rect.y = self.height - 100
            self.rect.x = index * button_width

        def update(self):
            nonlocal notes_clicked, score
            hits = pygame.sprite.spritecollide(self, note_sprites, False)

            for hit in hits:
                if pygame.key.get_pressed()[key_mapping["game_controls"][self.index]]:
                    if not hit.pressed:
                        logger.info(f"Hit! {self.index} Note Type: {hit.note_type}")
                        notes_clicked += 1
                        score += 100

                        hit.pressed = True

                    # HitImage(
                    #     all_sprites, x=hit.rect.x, y=hit.rect.y, creation_time=current_time
                    # )

    # Draw click buttons
    for i, pos in enumerate(button_positions):
        ClickButton(
            bottom_buttons_sprites,
            index=i
        )

    # Generate notes
    for note in notes:
        note_sprite = Note(
            button_width=button_width,
            column=note["column"],
            start_time=note["time"],
            note_type=note["type"]
        )
        note_sprites.add(note_sprite)

    # Game
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    music.stop()
                    return score, accuracy
            ui_manager.process_events(event)

        current_time = pygame.time.get_ticks() - start_time

        game_surface.fill(black)

        # Draw background
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(black)

        # Draw notes after drawing buttons
        note_sprites.update(current_time)
        note_sprites.draw(game_surface)

        all_sprites.update()
        all_sprites.draw(game_surface)

        # Draw buttons
        bottom_buttons_sprites.update()
        bottom_buttons_sprites.draw(game_surface)

        # Draw borders
        pygame.draw.rect(game_surface, white, (0, 0, 10, size[1]))
        pygame.draw.rect(game_surface, white, (game_surface_width - 10, 0, 10, size[1]))

        accuracy = (notes_clicked / total_notes) * 100 if 0 < total_notes else 100

        render_number(screen, f"{score:010}", (size[0] - 220, 20))
        render_text(screen, f"{accuracy:.2f}%", 35, (size[0] - 120, 80))

        # Draw game surface onto the screen
        screen.blit(game_surface, (150, 0))
        game_surface.set_alpha(240)

        if len(note_sprites) == 0:
            running = False

        pygame.display.flip()

        clock.tick(60)

    running = True

    class Rating_image(pygame.sprite.Sprite):
        def __init__(self, *group, rating_type):
            super().__init__(*group)

            self.image = load_image(f"skins/ranking-{rating_type}.png")
            self.image = pygame.transform.scale(self.image, (600, 600))

            self.rect = self.image.get_rect()
            self.rect.x = size[0] - 600
            self.rect.centery = size[1] // 2

    rating_type = get_rating(accuracy, rating)

    logger.warn(rating_type)

    Rating_image(all_sprites, rating_type=rating_type)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return score, accuracy

        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(black)

        render_number(screen, f"{score:010}", (200, size[1] // 2 - 100))
        render_number(screen, f"{accuracy:.2f}%", (200, size[1] // 2 + 100))

        all_sprites.draw(screen)

        pygame.display.flip()

        clock.tick(60)
