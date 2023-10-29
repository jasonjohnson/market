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

    def generate(self):
        if len(self.spices) == self.max_spices:
            return

        self.spices.append(Spice())

    def place(self):
        for s in self.spices:
            if s.get_parent():
                continue

            random_tile = self.tile_grid.get_random_tile()

            if not random_tile.has_resource_capacity():
                return

            random_tile.add_resource(s)

    def update(self, _delta):
        self.generate()
        self.place()
