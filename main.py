"""Main"""
import random
import time

import pygame

from lib import entity

WINDOW_CAPTION = "Market"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


def tile_distance(tile_a, tile_b):
    return abs(tile_a.row - tile_b.row) + abs(tile_a.column - tile_b.column)

def gather_entities(root_entity):
    entities = [root_entity]

    for entity in entities:
        entities.extend(entity.get_children())

    return entities

class TileGrid(entity.Entity):
    def __init__(self, rows, columns):
        super().__init__()
        self.tiles = []
        self.grid = []
        self.generate(rows, columns)
        self.link()

        for tile in self.tiles:
            self.add_child(tile)
    
    def get_tile(self, row, column):
        return self.grid[row][column]
    
    def get_random_tile(self):
        return random.choice(self.tiles)

    def generate(self, rows, columns):
        """Generate a 2-dimensional grid of tiles."""
        for r in range(rows):
            row = []
            for c in range(columns):
                tile = Tile(row=r, column=c)
                row.append(tile)

                # Build a list of all tiles. Helps when we need
                # to get a random tile and don't care where it is.
                self.tiles.append(tile)

            # Build the grid. Same tile references, just in a row
            # and column structure.
            self.grid.append(row)

    def link(self):
        """Link each tile in the tile grid to its neighbor to the north, south,
        east and west."""
        # Link each row east-to-west, bi-directionally.
        for row in self.grid:
            previous = None
            for i, tile in enumerate(row):
                tile.west = previous

                if i == len(row) - 1:
                    break

                tile.east = row[i + 1]
                previous = tile

        # Link each tile in a row north-to-south, bi-directionally.
        for i, row in enumerate(self.grid):
            for j, tile in enumerate(row):
                if i != 0:
                    tile.north = self.grid[i - 1][j]

                if i != len(self.grid) - 1:
                    tile.south = self.grid[i + 1][j]

    def inputs(self, events):
        pass

    def update(self, delta):
        pass

class Tile(entity.Entity):
    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column
        self.size = 50
        self.north = None
        self.south = None
        self.east = None
        self.west = None

    def get_neighbor_tiles(self):
        return list(filter(None, [self.north, self.south, self.east, self.west]))

    def get_child_of_kind(self, kind):
        for child in self.get_children():
            if isinstance(child, kind):
                return child
        return None

    def update(self, delta):
        pass

    def render(self, surface):
        pygame.draw.rect(
            surface,
            (40, 40, 40),
            (
                self.row * self.size,
                self.column * self.size,
                self.size,
                self.size,
            ),
            width=1
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

class World(entity.Entity):
    def __init__(self, tile_grid, spice_spawner):
        super().__init__()

        self.tile_grid = tile_grid
        self.spice_spawner = spice_spawner

        self.add_child(tile_grid)
        self.add_child(spice_spawner)

    def update(self, delta):
        pass

class Spice(entity.Entity):
    def __repr__(self):
        return "S"

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

class Harvester(entity.Entity):
    """Harvesters:
        [x] Spawn from a Base
        [x] Gather spice
        [x] Return spice to the Base they spawned at
    """
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.spice = None
        self.interval = 1.0
        self.interval_progress = 0.0

    def __repr__(self):
        if self.spice:
            return "H(S)"
        else:
            return "H( )"

    def find_spice(self, tile):
        tiles = tile.get_neighbor_tiles()
        goals = []

        for t in tiles:
            if t.get_child_of_kind(Spice):
                goals.append(t)

        tile.remove_child(self)

        if len(goals) > 0:
            random.choice(goals).add_child(self)
        else:
            random.choice(tiles).add_child(self)

    def collect_spice(self, tile, spice):
        tile.remove_child(spice)
        self.spice = spice

    def deposit_spice(self, tile, base):
        base.deposit_spice(self.spice)
        self.spice = None

    def find_base(self, tile):
        distance = tile_distance(tile, self.base.get_tile())
        distance_tile = tile

        tiles = tile.get_neighbor_tiles()
        goals = []

        for t in tiles:
            d = tile_distance(t, self.base.get_tile())
            if d < distance:
                distance = d
                distance_tile = t
            if t.get_child_of_kind(Base):
                goals.append(t)

        tile.remove_child(self)

        if len(goals) > 0:
            random.choice(goals).add_child(self)
        else:
            distance_tile.add_child(self)

    def update(self, delta):
        if self.interval_progress < self.interval:
            self.interval_progress += delta
            return

        tile = self.get_parent()

        if self.spice:
            base = tile.get_child_of_kind(Base)

            if base:
                self.deposit_spice(tile, base)
            else:
                self.find_base(tile)
        else:
            spice = tile.get_child_of_kind(Spice)

            if spice:
                self.collect_spice(tile, spice)
            else:
                self.find_spice(tile)

        self.interval_progress = 0.0

    def render(self, surface):
        pygame.draw.rect(
            surface,
            (0, 255, 0),
            (
                self.get_parent().row * self.get_parent().size + 7,
                self.get_parent().column * self.get_parent().size + 7,
                5,
                5,
            )
        )

class Base(entity.Entity):
    """Base:
        - [x] Spawns Harvesters
        - [x] Accept Spice from Harvesters
        - [x] Use Spice to create more Harvesters
    """
    def __init__(self, starting_spice):
        super().__init__()
        self.harvesters = []
        self.harvester_construction_cost = 1
        self.spices = []

        for s in range(starting_spice):
            self.spices.append(Spice())

    def __repr__(self):
        return "B"

    def get_tile(self):
        return self.get_parent()

    def deposit_spice(self, spice):
        self.spices.append(spice)

    def update(self, delta):
        if len(self.spices) >= self.harvester_construction_cost:
            del self.spices[:self.harvester_construction_cost]

            harvester = Harvester(self)

            self.harvesters.append(harvester)
            self.add_sibling(harvester)

if __name__ == "__main__":
    base = Base(
        starting_spice=1
    )

    tile_grid = TileGrid(10, 10)
    tile_grid.get_tile(0, 0).add_child(base)

    spice_spawner = SpiceSpawner(tile_grid, 10)

    world = World(
        tile_grid=tile_grid,
        spice_spawner=spice_spawner,
    )

    pygame.init()

    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption(WINDOW_CAPTION)

    events = []

    while True:
        delta = clock.tick() / 1000.0
        events.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            else:
                events.append(event)

        surface.fill((255, 255, 255))

        # Gathering this each time seems expensive, but it is the
        # most obvious way I can think of to keep the entity list
        # fresh (in case some are added/removed at run-time).
        entities = gather_entities(world)

        for e in entities:
            e.inputs(events)

        for e in entities:
            e.update(delta)

        for e in entities:
            e.render(surface)

        pygame.display.update()
