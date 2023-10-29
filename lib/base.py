import random

from . import entity, harvester, spice, sprite


class Base(entity.Entity):
    BASES = []

    def __init__(self, starting_spice):
        super().__init__()

        Base.BASES.append(self)

        self.sprites = sprite.SpriteSheet('tiles')
        self.harvesters = []
        self.harvester_construction_cost = 1
        self.spices = starting_spice

    def get_tile(self):
        return self.get_parent()

    def deposit_spice(self, spice_quantity):
        self.spices += spice_quantity
        self.emit('deposit')

    def debit_spice(self, spice_quantity) -> int:
        self.spices -= spice_quantity
        return self.spices

    def reduce_force(self) -> None:
        if self.spices >= 0:
            return

        reduction = int(abs(self.spices) / harvester.Harvester.UPKEEP_COST)

        for _ in range(reduction):
            h = random.choice(self.harvesters)
            h.self_destruct()

            self.harvesters.remove(h)

        # TODO this should self-regulate based on upkeep, but I'm keeping it simple
        #   to get the concept working.
        self.spices = 0

    def spawn_harvester(self):
        if self.spices < self.harvester_construction_cost:
            print('Not enough spices to build a harvester')
            return

        # Interesting. When the capacity is limited, spawning of the
        # same unit type is also inhibited! This is good.
        if not self.get_tile().has_unit_capacity():
            print('Not enough tile capacity to spawn a harvester')
            return

        new_harvester = harvester.Harvester(self)

        self.harvesters.append(new_harvester)

        self.get_tile().add_unit(new_harvester)

        self.emit('spawn')

        self.debit_spice(harvester.Harvester.SPAWN_COST)

    def compute_upkeep(self) -> int:
        return len(self.harvesters) * harvester.Harvester.UPKEEP_COST

    def render(self, surface):
        surface.blit(self.sprites.get_surface('desert_building'), self.get_position())
