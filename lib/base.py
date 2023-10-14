import pygame

from . import entity, harvester, spice

class Base(entity.Entity):
    def __init__(self, starting_spice):
        super().__init__(left=5, top=5)
        self.width = 10
        self.height = 10
        self.color = (0, 0, 0)
        self.rect = pygame.rect.Rect(
            self.get_left(),
            self.get_top(),
            self.width,
            self.height,
        )

        self.subscribe('spawn_request', self.handle_spawn_request)

        self.harvesters = []
        self.harvester_construction_cost = 1
        self.spices = []

        for s in range(starting_spice):
            self.deposit_spice(spice.Spice())

    def get_tile(self):
        return self.get_parent()

    def deposit_spice(self, spice):
        self.spices.append(spice)
        self.emit('deposit')

    def handle_spawn_request(self):
        if len(self.spices) < self.harvester_construction_cost:
            print("Not enough spices to build a harvester")
            return

        h = harvester.Harvester(self)

        self.harvesters.append(h)
        self.add_sibling(h)

        self.emit('spawn')

        del self.spices[:self.harvester_construction_cost]

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
            self.color,
            self.rect,
        )