import pygame

from . import entity

class Button(entity.Entity):
    def __init__(self):
        super().__init__()
        self.hovering = False
        self.color = (0, 0, 255)
        self.x = 510
        self.y = 0
        self.width = 200
        self.height = 20
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def inputs(self, events):
        for e in events:
            if e.type == pygame.MOUSEMOTION:
                self.hovering = self.rect.collidepoint(e.pos)
                self.on_mouse_hover()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if self.hovering and e.button == 1:
                    self.on_mouse_down()
            elif e.type == pygame.MOUSEBUTTONUP:
                if self.hovering and e.button == 1:
                    self.on_mouse_up()
                    self.on_mouse_click()

    def render(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            self.rect,
            width=1
        )

    def on_mouse_down(self):
        pass

    def on_mouse_up(self):
        pass

    def on_mouse_hover(self):
        pass

    def on_mouse_click(self):
        self.emit('spawn')
