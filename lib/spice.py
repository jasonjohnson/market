import pygame

from . import entity, sprite, tile


class Spice(entity.Entity):
    def __init__(self):
        super().__init__()
        self.sprites = sprite.SpriteSheet('tiles')

    def render(self, surface):
        if not isinstance(self.get_parent(), tile.Tile):
            return

        surface.blit(self.sprites.get_surface('desert_spice'), self.get_position())


class SpiceSpawner(entity.Entity):
    def __init__(self, tile_grid, max_spices):
        super().__init__()
        self.tile_grid = tile_grid
        self.max_spices = max_spices
        self.spices = []

    def update(self, _delta):
        if len(self.spices) == self.max_spices:
            return

        random_tile = self.tile_grid.get_random_tile()

        if not random_tile.has_resource_capacity():
            return

        spice = Spice()

        random_tile.add_resource(spice)
        self.spices.append(spice)
