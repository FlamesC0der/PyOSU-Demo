import pygame

from game.utils.image_loader import load_image
from log import logger


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