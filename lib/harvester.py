import collections
import random

from lib import base, spice, tile
from lib.core import automaton, entity, sprite


class Harvester(automaton.Automaton):
    SPAWN_COST = 1
    UPKEEP_COST = 1

    def __init__(self, spawn_base):
        super().__init__()

        self.sprites = sprite.SpriteSheet('tiles')
        self.spawn_base = spawn_base

        self.spice = None

        self.memory = collections.deque(maxlen=2)

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

        self.ref_delay = 5.0
        self.ref_delay_timer = 0.0

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
        tertiary = []

        for t in tiles:
            # Filter out any surrounding tile that doesn't have capacity.
            if not t.has_unit_capacity():
                continue

            # Spice is our objective. Prefer any tile containing spice.
            if t.get_child_of_kind(spice.Spice):
                primary.append(t)
            # Next, prefer tiles we don't remember.
            elif t not in self.memory:
                secondary.append(t)
            # Otherwise, any other tile.
            else:
                tertiary.append(t)

        self.move(primary, secondary, tertiary)

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
                t = random.choice(c)
                t.add_unit(self)

                self.memory.append(t)

                moved = True
                break

        if not moved:
            print('No moves available')

    def gather(self) -> None:
        found_spice = self.get_tile().get_child_of_kind(spice.Spice)

        self.get_tile().remove_child(found_spice)
        self.add_child(found_spice)
        self.spice = found_spice

    def deposit(self) -> None:
        found_base = self.get_tile().get_child_of_kind(base.Base)
        found_base.deposit_spice(1)

        self.remove_child(self.spice)
        self.spice = None

    def self_destruct(self):
        self.spice = None
        self.get_tile().add_child(HarvesterExplosion(
            self.get_left(),
            self.get_top()
        ))
        self.get_tile().remove_unit(self)

    def render(self, surface):
        surface.blit(self.sprites.get_surface('desert_harvester'), self.get_position())


class Particle:
    def __init__(self, particle_sprite, left, top):
        self.sprite = particle_sprite
        self.left = left
        self.left_speed = random.uniform(-0.5, 0.5)
        self.top = top
        self.top_speed = random.uniform(-0.5, 0.5)


class HarvesterExplosion(entity.Entity):
    def __init__(self, left=0, top=0):
        super().__init__(left=left, top=top)

        self.sprite = sprite.SpriteSheet('particles').get_surface('harvester')
        self.particles = []
        self.life = 1.0

        for _ in range(10):
            self.particles.append(Particle(
                self.sprite,
                left,
                top
            ))

    def is_alive(self):
        return self.life > 0.0

    def update(self, delta):
        if not self.is_alive():
            self.get_parent().remove_child(self)

        self.life -= delta
        self.sprite.set_alpha(int(self.life * 255))

        for p in self.particles:
            p.left += p.left_speed
            p.top += p.top_speed

    def render(self, surface):
        for p in self.particles:
            surface.blit(p.sprite, (p.left, p.top))
