import random

import pygame

from . import automaton, base, sprite, tile

class Builder(automaton.Automaton):
    def __init__(self, spawn_base):
        super().__init__()
        self.sprite = sprite.Sprite(5, 5)
        self.spawn_base = spawn_base
        self.wander_distance = 300

    def distance_from_base(self, t: tile.Tile):
        return tile.tile_distance(t, self.spawn_base.get_tile())

    def find_build_location(self, current_tile: tile.Tile, current_distance):
        tiles = current_tile.get_neighbor_tiles()
        goals = []

        for t in tiles:
            if self.distance_from_base(t) > current_distance:
                goals.append(t)

        current_tile.remove_child(self)

        random.choice(goals).add_child(self)

    def build_base(self, current_tile: tile.Tile):
        current_tile.add_child(base.Base(starting_spice=1))

    def self_destruct(self):
        self.get_parent().remove_child(self)

    def act(self):
        current_tile = self.get_parent()
        current_distance = self.distance_from_base(current_tile)

        if current_distance < self.wander_distance:
            self.find_build_location(current_tile, current_distance)
        else:
            self.build_base(current_tile)
            self.self_destruct()

    def render(self, surface: pygame.Surface):
        surface.blit(self.sprite.get_surface(), self.get_position())
