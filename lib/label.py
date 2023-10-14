import pygame

from . import entity

class Label(entity.Entity):
    def __init__(self, label):
        super().__init__(left=10, top=10)

        self.label = label
        self.text = ""
        self.color_text = (255, 255, 255)
        self.color_border = (0, 0, 255)
        self.font = pygame.font.Font(None, 14)
        self.harvesters = 0
        self.spice = 0
        self.rect = pygame.rect.Rect(
            self.get_left(),
            self.get_top(),
            0,
            0,
        )

        self.subscribe('deposit', self.handle_deposit)
        self.subscribe('spawn', self.handle_spawn)

    def handle_spawn(self):
        self.harvesters += 1
        self.spice -= 1

    def handle_deposit(self):
        self.spice += 1

    def update(self, delta):
        self.rect = pygame.rect.Rect(
            self.get_left(),
            self.get_top(),
            0,
            0,
        )

        self.text = self.label.format(
            harvesters=self.harvesters,
            spice=self.spice,
        )


    def render(self, surface):
        text = self.font.render(
            self.text, 1, self.color_text, self.color_border)

        surface.blit(text, self.rect)
