import pygame

from . import entity

class Spice(entity.Entity):
    def update(self, delta):
        pass

    def render(self, surface):
        if not hasattr(self.get_parent(), 'row'):
            return

        pygame.draw.rect(
            surface,
            (255, 0, 0),
            (
                self.get_parent().row * self.get_parent().size + 2,
                self.get_parent().column * self.get_parent().size + 2,
                5,
                5,
            )
        )

class SpiceSpawner(entity.Entity):
    def __init__(self, tile_grid, max_spices):
        super().__init__()
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

