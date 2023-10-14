import pygame

from . import entity, tile

class Spice(entity.Entity):
    def __init__(self):
        super().__init__(left=2, top=2)
        self.color = (255, 0, 0)
        self.width = 5
        self.height = 5
        self.rect = pygame.rect.Rect(
            self.get_left(),
            self.get_top(),
            self.width,
            self.height,
        )

    def update(self, delta):
        self.rect = pygame.rect.Rect(
            self.get_left(),
            self.get_top(),
            self.width,
            self.height,
        )

    def render(self, surface):
        if not isinstance(self.get_parent(), tile.Tile):
            return

        pygame.draw.rect(
            surface,
            self.color,
            self.rect,
        )

class SpiceSpawner(entity.Entity):
    def __init__(self, tile_grid, max_spices):
        super().__init__(left=0, top=0)
        self.tile_grid = tile_grid
        self.max_spices = max_spices
        self.spices = []

    def update(self, delta):
        if len(self.spices) == self.max_spices:
            return

        spice = Spice()

        tile = self.tile_grid.get_random_tile()
        tile.add_child(spice)

        self.spices.append(spice)
