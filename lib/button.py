import pygame

from . import entity

class Button(entity.Entity):
    def __init__(self, label, width=200, height=20):
        super().__init__(left=10, top=10)
        self.hovering = False
        self.color_text = (255, 255, 255)
        self.color_border = (0, 0, 255)
        self.label = label
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 14)
        self.rect = pygame.rect.Rect(
            self.get_left(),
            self.get_top(),
            self.width,
            self.height,
        )

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

    def update(self, delta):
        self.rect = pygame.rect.Rect(
            self.get_left(),
            self.get_top(),
            self.width,
            self.height,
        )

    def render(self, surface):
        pygame.draw.rect(
            surface,
            self.color_border,
            self.rect,
            width=3
        )

        text = self.font.render(
            self.label, 1, self.color_text, self.color_border)

        surface.blit(text, self.rect)

    def on_mouse_down(self):
        pass

    def on_mouse_up(self):
        pass

    def on_mouse_hover(self):
        pass

    def on_mouse_click(self):
        self.emit('spawn_request')
