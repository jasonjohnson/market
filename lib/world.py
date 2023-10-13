from . import entity

class World(entity.Entity):
    def __init__(self, tile_grid, spice_spawner):
        super().__init__()

        self.tile_grid = tile_grid
        self.spice_spawner = spice_spawner

        self.add_child(tile_grid)
        self.add_child(spice_spawner)

    def update(self, delta):
        pass
