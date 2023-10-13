from . import entity, harvester, spice

class Base(entity.Entity):
    def __init__(self, starting_spice):
        super().__init__()
        self.harvesters = []
        self.harvester_construction_cost = 1
        self.spices = []

        for s in range(starting_spice):
            self.spices.append(spice.Spice())

    def __repr__(self):
        return "B"

    def get_tile(self):
        return self.get_parent()

    def deposit_spice(self, spice):
        self.spices.append(spice)

    def update(self, delta):
        if len(self.spices) >= self.harvester_construction_cost:
            del self.spices[:self.harvester_construction_cost]

            h = harvester.Harvester(self)

            self.harvesters.append(h)
            self.add_sibling(h)