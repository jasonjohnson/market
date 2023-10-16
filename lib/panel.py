import pygame

from . import entity

class Panel(entity.Entity):
    def __init__(self, label, left, top, padding, width, height):
        super().__init__(left=left, top=top, padding=padding)

        self.label = label
        self.color_text = (255, 255, 255)
        self.color_border = (255, 0, 0)
        self.font = pygame.font.Font(None, 14)
        self.width = width
        self.height = height
        self.padding = padding

    def render(self, surface: pygame.Surface):
        rect = pygame.rect.Rect(
            self.get_left(),
            self.get_top(),
            self.width,
            self.height,
        )
        
        pygame.draw.rect(
            surface,
            self.color_border,
            rect,
            width=self.padding
        )

        text = self.font.render(
            self.label, 1, self.color_text, self.color_border)

        surface.blit(text, rect)
