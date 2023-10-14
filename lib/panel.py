import pygame

from . import entity

class Panel(entity.Entity):
    def __init__(self, label, left, top, width, height):
        super().__init__(left=left, top=top)

        self.label = label
        self.color_text = (255, 255, 255)
        self.color_border = (255, 0, 0)
        self.font = pygame.font.Font(None, 14)
        self.rect = pygame.rect.Rect(
            self.get_left(),
            self.get_top(),
            width,
            height,
        )

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(
            surface,
            self.color_border,
            self.rect,
            width=10
        )

        text = self.font.render(
            self.label, 1, self.color_text, self.color_border)

        surface.blit(text, self.rect)
