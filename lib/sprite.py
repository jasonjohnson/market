import pygame

class Sprite(object):
    def __init__(self, width, height):
        self.surface = pygame.Surface((width, height))
        self.width = width
        self.height = height
        self.debug_fill_color = pygame.Color('white')
        self.debug_border_color = pygame.Color('magenta')
        self.debug_border_width = 1

    def get_surface(self, debug=True):
        if debug:
            self.surface.fill(self.debug_fill_color)

            pygame.draw.rect(
                surface=self.surface,
                rect=self.surface.get_rect(),
                color=self.debug_border_color,
                width=self.debug_border_width,
            )

        return self.surface

    def get_global_rect(self, position):
        return self.surface.get_rect().move(position)
