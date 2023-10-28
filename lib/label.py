import pygame

from . import entity, sprite


class Label(entity.Entity):
    FONT_SIZE = 7

    def __init__(self, text, left=0, top=0):
        super().__init__(left=left, top=top)

        self.sprites = sprite.SpriteSheet('font')
        self.surface = pygame.Surface((len(text) * Label.FONT_SIZE, Label.FONT_SIZE), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()

        for i, c in enumerate(text):
            self.surface.blit(self.sprites.get_surface(c), (i * Label.FONT_SIZE, 0))

    def render(self, surface):
        surface.blit(self.surface, self.get_position())
