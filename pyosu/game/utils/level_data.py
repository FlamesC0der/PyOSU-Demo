import pygame
import os

from pyosu.game.utils.image_loader import load_image
from pyosu.log import logger
from pyosu.settings import MANIA_COLUMNS


def get_levels():
    # levels = [d for d in os.listdir('songs') if os.path.isdir(os.path.join('songs', d))]
    levels = []
    for song in os.listdir('songs'):
        if os.path.isdir(os.path.join('songs', song)):
            bg, music, tickrate, notes = load_level_data(song)
            levels.append({
                "name": song,
                "bg": bg,
                "music": music
            })
    return levels


def load_level_data(name):
    music, bg, tickrate, notes = None, None, 1, []

    with open(f"songs/{name}/data.osu", "r") as f:
        general = False
        difficulty = False
        hit_objects = False
        for line in list(map(lambda s: s.strip(), f.readlines())):
            if "[General]" in line:
                general = True
            elif "[Difficulty]" in line:
                general = False
                difficulty = True
            elif "[HitObjects]" in line:
                difficulty = False
                hit_objects = True
            elif general and line:
                if "AudioFilename" in line:
                    try:
                        music = pygame.mixer.Sound(f"songs/{name}/{line.split(': ')[1]}")
                    except Exception as e:
                        logger.error("Failed to load music")
            elif difficulty and line:
                if "SliderTickRate" in line:
                    tickrate = int(line.split(":")[1])

            elif hit_objects and line:
                values = line.split(",")

                time = int(values[2])
                column = int(values[0]) % MANIA_COLUMNS
                note_type = int(values[3])

                notes.append({"time": time, "column": column, "type": note_type})

    try:
        bg = load_image(f"songs/{name}/bg.jpg")
    except Exception as e:
        logger.error("Failed to load bg")

    return bg, music, tickrate, notes
