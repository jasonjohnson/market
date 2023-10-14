import random

import pygame

from . import entity

def tile_distance(tile_a, tile_b):
    return abs(tile_a.get_top() - tile_b.get_top()) + \
        abs(tile_a.get_left() - tile_b.get_left())

class TileGrid(entity.Entity):
    def __init__(self, rows, columns):
        super().__init__(left=10, top=10)
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
        self.width = 20
        self.height = 20

        super().__init__(left=(column * self.width), top=(row * self.height))

        self.north = None
        self.south = None
        self.east = None
        self.west = None
        
        # https://www.pygame.org/docs/ref/color_list.html
        self.color = pygame.color.Color('azure3')
        self.rect = pygame.rect.Rect(
            self.get_left(),
            self.get_top(),
            self.width,
            self.height,
        )

    def get_neighbor_tiles(self):
        return list(filter(None, [self.north, self.south, self.east, self.west]))

    def get_child_of_kind(self, kind):
        for child in self.get_children():
            if isinstance(child, kind):
                return child
        return None

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
            width=1
        )
