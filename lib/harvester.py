import random

from . import automaton, base, spice, sprite, tile


class Harvester(automaton.Automaton):
    def __init__(self, spawn_base):
        super().__init__()

        self.sprite = sprite.Sprite(5, 5)
        self.spawn_base = spawn_base

        self.spice = None

        self.add_state('finding', initial=True)
        self.add_state('gathering', on_enter=self.gather)
        self.add_state('delivering')
        self.add_state('depositing', on_enter=self.deposit)

        self.add_transition(
            state_a='finding',
            state_b='gathering',
            test=self.can_gather,
            on_failure=self.move_toward_spice,
        )

        self.add_transition(
            state_a='gathering',
            state_b='delivering',
            test=self.can_deliver,
        )

        self.add_transition(
            state_a='delivering',
            state_b='depositing',
            test=self.can_deposit,
            on_failure=self.move_toward_base,
        )

        self.add_transition(
            state_a='depositing',
            state_b='finding',
            test=self.can_repeat,
        )

    def get_tile(self) -> tile.Tile:
        return self.get_parent()

    def get_base_tile(self) -> tile.Tile:
        return self.spawn_base.get_tile()

    def can_gather(self) -> bool:
        return self.get_tile().get_child_of_kind(spice.Spice) is not None

    def can_deliver(self) -> bool:
        return self.spice is not None

    def can_deposit(self) -> bool:
        return self.get_tile().get_child_of_kind(base.Base) is not None

    def can_repeat(self) -> bool:
        return True

    def move_toward_spice(self) -> None:
        tiles = self.get_tile().get_neighbor_tiles()
        tiles_objective = []

        for t in tiles:
            if t.get_child_of_kind(spice.Spice):
                tiles_objective.append(t)

        self.get_tile().remove_child(self)

        if len(tiles_objective) > 0:
            random.choice(tiles_objective).add_child(self)
        else:
            random.choice(tiles).add_child(self)

    def move_toward_base(self) -> None:
        current = self.get_tile()
        current_distance = tile.tile_distance(current, self.get_base_tile())

        tiles = current.get_neighbor_tiles()
        tiles_objective = []
        tiles_closer = []

        for t in tiles:
            d = tile.tile_distance(t, self.get_base_tile())

            if d < current_distance:
                tiles_closer.append(t)

            if t.get_child_of_kind(base.Base):
                tiles_objective.append(t)

        self.get_tile().remove_child(self)

        if len(tiles_objective) > 0:
            random.choice(tiles_objective).add_child(self)
        else:
            random.choice(tiles_closer).add_child(self)

    def gather(self) -> None:
        found_spice = self.get_tile().get_child_of_kind(spice.Spice)

        self.get_tile().remove_child(found_spice)
        self.spice = found_spice

    def deposit(self) -> None:
        found_base = self.get_tile().get_child_of_kind(base.Base)
        found_base.deposit_spice(self.spice)

        self.spice = None

    def render(self, surface):
        surface.blit(self.sprite.get_surface(), self.get_position())
