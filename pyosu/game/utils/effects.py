import pygame


class Fader:
    def __init__(self, screen, width, height, fade_speed=5):
        self.screen = screen
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.fade_speed = fade_speed
        self.fade_out_complete = False

    def fade_in(self):
        fade_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for alpha in range(255, 0, -self.fade_speed):
            fade_surface.fill((0, 0, 0, alpha))
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        running = True
        elapsed_time = 0
        fade_duration = 2000

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))

            elapsed_time += self.clock.tick(60)
            if elapsed_time >= fade_duration and not self.fade_out_complete:
                self.fade_in()
                self.fade_out_complete = True

            pygame.display.flip()

            if self.fade_out_complete:
                break
