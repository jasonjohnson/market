import pygame

from . import entity, harvester, spice, sprite


class Base(entity.Entity):
    BASES = []

    def __init__(self, starting_spice):
        super().__init__()

        self.sprites = sprite.SpriteSheet('tiles')
        self.harvesters = []
        self.harvester_construction_cost = 1
        self.spices = []

        for _ in range(starting_spice):
            self.deposit_spice(spice.Spice())

        Base.BASES.append(self)

    def __del__(self):
        # This shouldn't happen, but will probably be important
        # when bases can be destroyed.
        Base.BASES.remove(self)

    def get_tile(self):
        return self.get_parent()

    def deposit_spice(self, new_spice):
        self.spices.append(new_spice)
        self.emit('deposit')

    def spawn_harvester(self):
        if len(self.spices) < self.harvester_construction_cost:
            print('Not enough spices to build a harvester')
            return

        # Interesting. When the capacity is limited, spawning of the
        # same unit type is also inhibited! This is good.
        if not self.get_tile().has_unit_capacity():
            print('No capacity to spawn a harvester')
            return

        new_harvester = harvester.Harvester(self)

        self.harvesters.append(new_harvester)

        self.get_tile().add_unit(new_harvester)

        self.emit('spawn')

        del self.spices[:self.harvester_construction_cost]

    def render(self, surface):
        surface.blit(self.sprites.get_surface('desert_building'), self.get_position())
