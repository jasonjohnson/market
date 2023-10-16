import random

from . import base, entity, spice, sprite, tile

class Harvester(entity.Entity):
    def __init__(self, spawn_base):
        super().__init__(left=2, top=2)

        self.sprite = sprite.Sprite(5, 5)
        self.spawn_base = spawn_base
        self.spice = None
        self.interval = 0.2
        self.interval_progress = 0.0

    def find_spice(self, tile):
        tiles = tile.get_neighbor_tiles()
        goals = []

        for t in tiles:
            if t.get_child_of_kind(spice.Spice):
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

    def find_base(self, current_tile):
        distance = tile.tile_distance(current_tile,
                                      self.spawn_base.get_tile())
        distance_tile = current_tile

        tiles = current_tile.get_neighbor_tiles()
        goals = []

        for t in tiles:
            d = tile.tile_distance(t, self.spawn_base.get_tile())
            if d < distance:
                distance = d
                distance_tile = t
            if t.get_child_of_kind(base.Base):
                goals.append(t)

        current_tile.remove_child(self)

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
            b = tile.get_child_of_kind(base.Base)

            if b:
                self.deposit_spice(tile, b)
            else:
                self.find_base(tile)
        else:
            s = tile.get_child_of_kind(spice.Spice)

            if s:
                self.collect_spice(tile, s)
            else:
                self.find_spice(tile)

        self.interval_progress = 0.0

    def render(self, surface):
        surface.blit(self.sprite.get_surface(), self.get_position())
