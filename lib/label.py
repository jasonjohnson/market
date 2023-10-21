import pygame

from . import base, entity, sprite


class Label(entity.Entity):
    def __init__(self, text, width=200, height=20):
        super().__init__(left=10, top=10)

        self.sprite = sprite.Sprite(width, height)
        self.color = pygame.Color('magenta')
        self.font = pygame.font.Font(None, 14)
        self.text = text
        self.harvesters = 0
        self.spice = 0

        self.subscribe('deposit', self.handle_base_activity)
        self.subscribe('spawn', self.handle_base_activity)

    def handle_base_activity(self):
        self.harvesters = 0
        self.spice = 0

        for b in base.Base.BASES:
            self.harvesters += len(b.harvesters)
            self.spice += len(b.spices)

    def render(self, surface):
        label = self.font.render(
            self.text.format(
                harvesters=self.harvesters,
                spice=self.spice,
            ),
            False,
            self.color
        )

        surface.blit(label, self.get_position())
