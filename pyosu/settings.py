import pygame

from game.utils.image_loader import load_image

MANIA_COLUMNS = 5

key_mapping = {
    "game_controls": {
        3: {
            0: pygame.K_a,
            1: pygame.K_SPACE,
            2: pygame.K_l
        },
        4: {
            0: pygame.K_a,
            1: pygame.K_s,
            2: pygame.K_k,
            3: pygame.K_l
        },
        5: {
            0: pygame.K_a,
            1: pygame.K_s,
            2: pygame.K_SPACE,
            3: pygame.K_k,
            4: pygame.K_l
        },
        6: {
            0: pygame.K_a,
            1: pygame.K_s,
            2: pygame.K_d,
            3: pygame.K_j,
            4: pygame.K_k,
            5: pygame.K_l
        },
        7: {
            0: pygame.K_a,
            1: pygame.K_s,
            2: pygame.K_d,
            3: pygame.K_SPACE,
            4: pygame.K_j,
            5: pygame.K_k,
            6: pygame.K_l
        }
    }
}

rating = {
    100: "X",
    95: "S",
    90: "A",
    80: "B",
    60: "C",
    0: "D"
}


def get_notes_images():
    return {
        3: [
            load_image("skins/mania-note1.png"),
            load_image("skins/mania-note2.png"),
            load_image("skins/mania-note1.png")
        ],
        4: [
            load_image("skins/mania-note1.png"),
            load_image("skins/mania-note2.png"),
            load_image("skins/mania-note3.png"),
            load_image("skins/mania-note1.png")
        ],
        5: [
            load_image("skins/mania-note1.png"),
            load_image("skins/mania-note2.png"),
            load_image("skins/mania-note3.png"),
            load_image("skins/mania-note2.png"),
            load_image("skins/mania-note1.png")
        ],
        6: [
            load_image("skins/mania-note1.png"),
            load_image("skins/mania-note2.png"),
            load_image("skins/mania-note3.png"),
            load_image("skins/mania-note1.png"),
            load_image("skins/mania-note2.png"),
            load_image("skins/mania-note1.png")
        ],
        7: [
            load_image("skins/mania-note1.png"),
            load_image("skins/mania-note2.png"),
            load_image("skins/mania-note1.png"),
            load_image("skins/mania-note3.png"),
            load_image("skins/mania-note1.png"),
            load_image("skins/mania-note2.png"),
            load_image("skins/mania-note1.png"),
        ]
    }
