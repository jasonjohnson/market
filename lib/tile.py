import random

import pygame

from . import entity, sprite


def tile_distance(tile_a, tile_b):
    return abs(tile_a.get_top() - tile_b.get_top()) + \
        abs(tile_a.get_left() - tile_b.get_left())


class TileGrid(entity.Entity):
    def __init__(self, rows, columns):
        super().__init__(left=10, top=10)

        self.sprite = sprite.Sprite(rows * Tile.SIZE, columns * Tile.SIZE)
        self.selected = None
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

    def is_hovering(self, position):
        return self.sprite.get_global_rect(
            self.get_position()).collidepoint(position)

    def inputs(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP:
                if self.is_hovering(e.pos) and e.button == 1:
                    left, top = e.pos
                    self.on_mouse_click(left, top)

    def render(self, surface):
        surface.blit(self.sprite.get_surface(), self.get_position())

    def on_mouse_click(self, global_left, global_top):
        offset_left, offset_top = self.get_position()

        local_left = global_left - offset_left
        local_top = global_top - offset_top

        row = int(local_top / Tile.SIZE)
        column = int(local_left / Tile.SIZE)

        if self.selected:
            self.selected.deselect()

        self.selected = self.grid[row][column]
        self.selected.select()

        self.emit('change_tile_selection', self.selected)


class Tile(entity.Entity):
    SIZE = 20

    def __init__(self, row, column):
        left = column * Tile.SIZE
        top = row * Tile.SIZE
        super().__init__(left=left, top=top)

        self.sprite_selected = sprite.Sprite(Tile.SIZE, Tile.SIZE, pygame.Color('black'))
        self.sprite_default = sprite.Sprite(Tile.SIZE, Tile.SIZE)
        self.sprites = sprite.SpriteSheet('tiles')
        self.selected = False
        self.row = row
        self.column = column
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.building = None
        self.resource = None
        self.unit = None

    def get_neighbor_tiles(self):
        return list(filter(None, [self.north, self.south, self.east, self.west]))

    def get_child_of_kind(self, kind):
        for child in self.get_children():
            if isinstance(child, kind):
                return child
        return None

    def has_unit_capacity(self) -> bool:
        if self.unit:
            return False
        return True

    def add_unit(self, unit) -> None:
        if not self.has_unit_capacity():
            raise ValueError('No unit capacity')
        self.unit = unit
        self.add_child(unit)

    def remove_unit(self, unit) -> None:
        self.unit = None
        self.remove_child(unit)

    def has_building_capacity(self) -> bool:
        if self.building:
            return False
        return True

    def add_building(self, building) -> None:
        if not self.has_building_capacity():
            raise ValueError('No building capacity')
        self.building = building
        self.add_child(building)

    def remove_building(self, building) -> None:
        self.building = None
        self.remove_child(building)

    def has_resource_capacity(self) -> bool:
        if self.resource:
            return False
        return True

    def add_resource(self, resource) -> None:
        if not self.has_resource_capacity():
            raise ValueError('No resource capacity')
        self.resource = resource
        self.add_child(resource)

    def remove_resource(self, resource) -> None:
        self.resource = None
        self.remove_child(resource)

    def render(self, surface):
        # TODO add selected sprite state
        surface.blit(self.sprites.get_surface('desert'), self.get_position())

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False
