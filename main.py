"""Main"""
import random
import time

import pygame

from lib import base, entity, spice, tile, world

WINDOW_CAPTION = "Market"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

if __name__ == "__main__":
    base = base.Base(
        starting_spice=1
    )

    tile_grid = tile.TileGrid(10, 10)
    tile_grid.get_tile(0, 0).add_child(base)

    spice_spawner = spice.SpiceSpawner(tile_grid, 10)

    world = world.World(
        tile_grid=tile_grid,
        spice_spawner=spice_spawner,
    )

    pygame.init()

    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption(WINDOW_CAPTION)

    events = []

    while True:
        delta = clock.tick() / 1000.0
        events.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            else:
                events.append(event)

        surface.fill((255, 255, 255))

        # Gathering this each time seems expensive, but it is the
        # most obvious way I can think of to keep the entity list
        # fresh (in case some are added/removed at run-time).
        entities = entity.gather_entities(world)

        for e in entities:
            e.inputs(events)

        for e in entities:
            e.update(delta)

        for e in entities:
            e.render(surface)

        pygame.display.update()
