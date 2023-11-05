import pygame

from lib.core import entity, sprite


class Label(entity.Entity):
    FONT_SIZE = 7

    def __init__(self, text, left=0, top=0):
        super().__init__(left=left, top=top)

        self.text = text
        self.width = len(text) * Label.FONT_SIZE
        self.height = Label.FONT_SIZE
        self.sprites = sprite.SpriteSheet('gui_debug')
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()

        for i, c in enumerate(text):
            self.surface.blit(self.sprites.get_surface(c), (i * Label.FONT_SIZE, 0))

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def render(self, surface):
        surface.blit(self.surface, self.get_position())
