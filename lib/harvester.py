import random

import pygame

from . import automaton, base, spice, sprite, tile


class Harvester(automaton.Automaton):
    def __init__(self, spawn_base):
        super().__init__()

        self.sprites = sprite.SpriteSheet('tiles')
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
        primary = []
        secondary = []

        for t in tiles:
            # Filter out any surrounding tile that doesn't have capacity.
            if not t.has_unit_capacity():
                continue

            # Spice is our objective. Prefer any tile containing spice.
            if t.get_child_of_kind(spice.Spice):
                primary.append(t)
            # Otherwise, any other tile.
            else:
                secondary.append(t)

        self.move(primary, secondary)

    def move_toward_base(self) -> None:
        current = self.get_tile()
        current_distance = tile.tile_distance(current, self.get_base_tile())

        tiles = current.get_neighbor_tiles()
        primary = []
        secondary = []
        tertiary = []

        for t in tiles:
            # Filter out any surrounding tile that doesn't have capacity.
            if not t.has_unit_capacity():
                continue

            # The base is our objective. Prefer a tile containing our
            # spawn base.
            #   TODO check that this base matches our spawn base
            if t.get_child_of_kind(base.Base):
                primary.append(t)
            # Alternatively, move closer to our spawn base.
            elif tile.tile_distance(t, self.get_base_tile()) < current_distance:
                secondary.append(t)
            # Otherwise, any other tile.
            else:
                tertiary.append(t)

        self.move(primary, secondary, tertiary)

    def move(self, *args) -> None:
        moved = False

        for c in args:
            if len(c) > 0:
                self.get_tile().remove_unit(self)
                random.choice(c).add_unit(self)

                moved = True
                break

        if not moved:
            print('No moves available')

    def gather(self) -> None:
        found_spice = self.get_tile().get_child_of_kind(spice.Spice)

        self.get_tile().remove_child(found_spice)
        self.spice = found_spice

    def deposit(self) -> None:
        found_base = self.get_tile().get_child_of_kind(base.Base)
        found_base.deposit_spice(self.spice)

        self.spice = None

    def render(self, surface):
        surface.blit(self.sprites.get_surface('desert_unit'), self.get_position())
