import random

from . import automaton, base, sprite, tile


class Builder(automaton.Automaton):
    def __init__(self, spawn_base):
        super().__init__()

        self.sprite = sprite.Sprite(5, 5)
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
        return self.distance_from_base() > self.wander_distance

    def can_destroy(self) -> bool:
        if not self.has_built:
            return False
        return True

    def move_toward_build_site(self):
        tiles = self.get_tile().get_neighbor_tiles()
        tile_options = []

        for t in tiles:
            if self.distance_from_base(t) > self.distance_from_base():
                tile_options.append(t)

        self.get_tile().remove_child(self)

        random.choice(tile_options).add_child(self)

    def build(self):
        self.get_tile().add_child(base.Base(starting_spice=1))
        self.has_built = True

    def destroy(self):
        self.get_parent().remove_child(self)

    def render(self, surface):
        surface.blit(self.sprite.get_surface(), self.get_position())
