from . import entity, harvester, spice, sprite


class Base(entity.Entity):
    def __init__(self, starting_spice):
        super().__init__(left=5, top=5)

        self.sprite = sprite.Sprite(10, 10)
        self.harvesters = []
        self.harvester_construction_cost = 1
        self.spices = []

        for _ in range(starting_spice):
            self.deposit_spice(spice.Spice())

        self.subscribe('spawn_request', self.handle_spawn_request)

    def get_tile(self):
        return self.get_parent()

    def deposit_spice(self, new_spice):
        self.spices.append(new_spice)
        self.emit('deposit')

    def handle_spawn_request(self):
        if len(self.spices) < self.harvester_construction_cost:
            print("Not enough spices to build a harvester")
            return

        new_harvester = harvester.Harvester(self)

        self.harvesters.append(new_harvester)
        self.add_sibling(new_harvester)

        self.emit('spawn')

        del self.spices[:self.harvester_construction_cost]

    def render(self, surface):
        surface.blit(self.sprite.get_surface(), self.get_position())
