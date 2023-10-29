import random

from . import automaton, base, sprite, tile


class Builder(automaton.Automaton):
    def __init__(self, spawn_base):
        super().__init__()

        self.sprites = sprite.SpriteSheet('tiles')
        self.spawn_base = spawn_base

        self.wander_distance = 300
        self.has_built = False

        self.add_state('moving', initial=True)
        self.add_state('building', on_enter=self.build)
        self.add_state('destroying', on_enter=self.destroy)

        self.add_transition(
            state_a='moving',
            state_b='building',
            test=self.can_build,
            on_failure=self.move_toward_build_site,
        )

        self.add_transition(
            state_a='building',
            state_b='destroying',
            test=self.can_destroy,
        )

    def get_tile(self):
        return self.get_parent()

    def distance_from_base(self, tile_a=None):
        if not tile_a:
            tile_a = self.get_tile()

        return tile.tile_distance(tile_a, self.spawn_base.get_tile())

    def can_build(self) -> bool:
        if not self.get_tile().has_building_capacity():
            return False
        return self.distance_from_base() > self.wander_distance

    def can_destroy(self) -> bool:
        if not self.has_built:
            return False
        return True

    def move_toward_build_site(self):
        tiles = self.get_tile().get_neighbor_tiles()
        primary = []
        secondary = []

        for t in tiles:
            if not t.has_unit_capacity():
                continue

            if self.distance_from_base(t) > self.distance_from_base():
                primary.append(t)
            else:
                secondary.append(t)

        self.move(primary, secondary)

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

    def build(self):
        self.get_tile().add_child(base.Base(starting_spice=1))
        self.has_built = True

    def destroy(self):
        self.get_tile().remove_unit(self)

    def render(self, surface):
        surface.blit(self.sprites.get_surface('desert_builder'), self.get_position())
