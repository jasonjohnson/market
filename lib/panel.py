import pygame

from . import entity, sprite


class Panel(entity.Entity):
    def __init__(self, text, left, top, width, height):
        super().__init__(left=left, top=top)

        self.sprite = sprite.Sprite(width, height)
        self.color = pygame.Color('magenta')
        self.font = pygame.font.Font(None, 14)
        self.text = text

    def render(self, surface: pygame.Surface):
        label = self.font.render(self.text, False, self.color)

        surface.blit(self.sprite.get_surface(), self.get_position())
        surface.blit(label, self.get_position())
