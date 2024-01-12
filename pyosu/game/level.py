import sys
import random
import pygame

from pyosu.game.resources.colors import *
from pyosu.game.utils.image_loader import load_image
from pyosu.game.utils.rating import get_rating
from pyosu.game.utils.fonts import render_text, render_number
from pyosu.game.utils.level_data import load_level_data
from pyosu.game.utils.effects import Fader
from pyosu.game.sprites import Rating_image, Result_types, Back_Button
from pyosu.settings import key_mapping, rating, MANIA_COLUMNS, get_notes_images
from pyosu.game.core import Cursor, cursor_change
from pyosu.log import logger

clock = pygame.time.Clock()


def play_level(screen, ui_manager, size, name):
    global total_notes
    logger.info("")
    logger.info(f"Play level {name}")

    cursor = Cursor(screen)

    fader = Fader(screen, size[0], size[1])

    game_surface_width = 100 * MANIA_COLUMNS
    game_surface = pygame.Surface((game_surface_width, size[1]))

    button_width = game_surface_width // MANIA_COLUMNS

    button_positions = [(i * button_width, size[1] - 50) for i in range(MANIA_COLUMNS)]

    running = True

    bg, music, tickrate, notes = load_level_data(name)
    logger.info("Data loaded")

    if bg:
        bg = pygame.transform.scale(bg, size)
    if music:
        music.play()

    start_time = pygame.time.get_ticks()

    logger.info("Starting level")

    # Stats
    logger.info(f"Total notes: {len(notes)}")
    scores = {
        300: 0,
        200: 0,
        100: 0,
        0: 0
    }
    score = 0
    combo = 0
    total_notes = 0
    notes_clicked = 0
    accuracy = 0

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    hit_sprites = pygame.sprite.Group()
    note_sprites = pygame.sprite.Group()
    bottom_buttons_sprites = pygame.sprite.Group()

    notes_images = get_notes_images()

    class HitImage(pygame.sprite.Sprite):
        def __init__(self, *groups, creation_time, type):
            super().__init__(*groups)

            if type == 300:
                if random.randint(0, 1):
                    type = f"{type}"
                else:
                    type = f"{type}g-0"

            self.image = load_image(f"skins/mania-hit{type}.png")
            self.rect = self.image.get_rect()
            self.rect.centerx = game_surface_width // 2
            self.rect.centery = size[1] // 2

            # self.creation_time = creation_time

        def update(self):
            pass
            # if pygame.time.get_ticks() - self.creation_time >= 10000:
            #     self.kill()

    class Note(pygame.sprite.Sprite):
        def __init__(self, *groups, image, button_width, column, start_time, note_type, tickrate):
            super().__init__(*groups)

            self.image = image
            self.image = pygame.transform.scale(self.image, (button_width, 30))

            self.rect = self.image.get_rect()
            self.rect.x = column * 100
            self.rect.y = 0

            self.column = column
            self.tickrate = 1000 / tickrate

            self.time = start_time
            self.note_type = note_type
            self.start_time = start_time - self.tickrate
            self.height = size[1]

        def update(self, current_time):
            global total_notes
            nonlocal combo
            progress = min(1, (current_time - self.start_time) / self.tickrate)
            self.rect.y = int(progress * self.height)

            if self.rect.y >= size[1] - 50:
                total_notes += 1
                self.kill()

                combo = 0
                scores[0] += 1

                for spite in all_sprites:
                    spite.kill()

                HitImage(
                    all_sprites, hit_sprites, creation_time=current_time, type=0
                )

    class ClickButton(pygame.sprite.Sprite):
        def __init__(self, *groups, index):
            super().__init__(*groups)

            self.image = load_image("skins/mania-key1.png")
            self.image = pygame.transform.scale(self.image, (button_width, 200))
            self.rect = self.image.get_rect()

            self.index = index
            self.height = size[1]

            self.rect.y = self.height - 200
            self.rect.x = index * button_width

            self.rect.h = 80

            self.clicked = False

            self.hitboxes = [
                {"min": 650, "max": 690, "score": 100},  # Good
                {"min": 691, "max": 720, "score": 200},  # Great
                {"min": 721, "max": 750, "score": 300},  # Excellent
                {"min": 751, "max": 780, "score": 200},  # Great
                {"min": 781, "max": 820, "score": 100},  # Good
            ]

        def update(self):
            nonlocal notes_clicked, score, combo, scores
            global total_notes
            hits = pygame.sprite.spritecollide(self, note_sprites, False)

            if pygame.key.get_pressed()[key_mapping["game_controls"][MANIA_COLUMNS][self.index]]:
                self.clicked = True
            else:
                self.clicked = False

            if self.clicked:
                self.image = load_image("skins/mania-key1D.png")
            else:
                self.image = load_image("skins/mania-key1.png")
            self.image = pygame.transform.scale(self.image, (button_width, 200))

            for hitbox in self.hitboxes:
                for hit in hits:
                    # logger.warning(hit.rect.y)
                    if (pygame.key.get_pressed()[key_mapping["game_controls"][MANIA_COLUMNS][self.index]]) \
                            and hitbox["min"] <= hit.rect.y <= hitbox['max']:
                        logger.info(f"Hit! {self.index} Note Type: {hit.note_type}")
                        notes_clicked += 1
                        combo += 1
                        score += hitbox["score"]
                        scores[hitbox["score"]] += 1

                        pygame.mixer.music.load("skins/drum-hitnormal.wav")
                        pygame.mixer.music.play()

                        hit.kill()
                        total_notes += 1
                        for spite in all_sprites:
                            spite.kill()

                        HitImage(
                            all_sprites, hit_sprites, creation_time=current_time, type=hitbox["score"]
                        )

    # Draw click buttons
    for i, pos in enumerate(button_positions):
        ClickButton(
            bottom_buttons_sprites,
            index=i
        )

    # Generate notes
    for note in notes:
        Note(
            note_sprites,
            image=notes_images[MANIA_COLUMNS][note["column"]],
            button_width=button_width,
            column=note["column"],
            start_time=note["time"],
            note_type=note["type"],
            tickrate=tickrate
        )

    # Game
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    music.stop()
                    return 0, 0
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
        pygame.draw.rect(game_surface, (80, 34, 99), (0, size[1] - 200, game_surface_width, 10))

        pygame.draw.rect(game_surface, white, (0, 0, 10, size[1]))
        pygame.draw.rect(game_surface, white, (game_surface_width - 10, 0, 10, size[1]))

        accuracy = (notes_clicked / total_notes) * 100 if 0 < total_notes else 100

        render_number(game_surface, f"{combo}", (game_surface_width // 2 - 10, size[1] // 2 - 100), combo=True)

        render_number(screen, f"{score:010}", (size[0] - 220, 20))
        render_text(screen, f"{accuracy:.2f}%", 35, (size[0] - 120, 80))

        # Draw game surface onto the screen
        screen.blit(game_surface, (150, 0))
        game_surface.set_alpha(240)

        hit_sprites.update()
        hit_sprites.draw(game_surface)

        if len(note_sprites) == 0:
            running = False

        cursor.update()

        pygame.display.flip()

        clock.tick(60)

    for sprite in all_sprites:
        sprite.kill()

    running = True

    fader.run()

    rating_type = get_rating(accuracy, rating)

    back_button = Back_Button(all_sprites, size=size)

    Rating_image(all_sprites, rating_type=rating_type, x=size[0] - 600, y=size[1] // 2)
    Rating_image(all_sprites, rating_type=rating_type, x=size[0] - 570, y=size[1] // 2 + 30)

    Result_types(all_sprites, rating_type=300, x=300, y=size[1] // 2 - 200)
    Result_types(all_sprites, rating_type=200, x=350, y=size[1] // 2 - 100)
    Result_types(all_sprites, rating_type=100, x=350, y=size[1] // 2)
    Result_types(all_sprites, rating_type=0, x=350, y=size[1] // 2 + 100)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    music.stop()
                    return score, accuracy
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_button.rect.collidepoint(event.pos):
                        fader.run()
                        return score, accuracy

        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(black)

        # Result
        render_number(screen, f"{score:010}", (300, size[1] // 2 - 300))

        render_number(screen, str(scores[300]), (550, size[1] // 2 - 200))
        render_number(screen, str(scores[200]), (550, size[1] // 2 - 100))
        render_number(screen, str(scores[100]), (550, size[1] // 2))
        render_number(screen, str(scores[0]), (550, size[1] // 2 + 100))

        render_number(screen, f"{accuracy:.2f}%", (350, size[1] // 2 + 200))
        render_number(screen, f"{combo}", (150, size[1] // 2 + 200))

        all_sprites.draw(screen)

        cursor.update()

        pygame.display.flip()

        clock.tick(60)
