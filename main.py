"""Main"""
import random
import time

import pygame

from lib import base, button, builder, entity, label, panel, spice, tile, world

WINDOW_CAPTION = "Market"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

if __name__ == "__main__":
    pygame.init()

    panel_spice_field = panel.Panel(
        text="SPICE FIELD",
        left=280,
        top=0,
        width=720,
        height=720,
    )

    tile_grid = tile.TileGrid(35, 35)

    # 10% of tiles have spice. No idea if this is a good value.
    spice_spawner = spice.SpiceSpawner(tile_grid, int((35 * 35) * 0.1))

    panel_spice_field.add_child(tile_grid)
    panel_spice_field.add_child(spice_spawner)

    panel_actions = panel.Panel(
        text="ACTIONS",
        left=1000,
        top=0,
        width=280,
        height=720,
    )

    panel_actions.add_child(button.Button("SPAWN HARVESTER"))

    panel_economy = panel.Panel(
        text="ECONOMY",
        left=0,
        top=480,
        width=280,
        height=240,
    )
    panel_economy.add_child(label.Label("Harvesters: {harvesters} Spice: {spice}"))

    world = world.World()
    world.add_child(panel_spice_field)
    world.add_child(panel_actions)
    world.add_child(panel_economy)
    world.add_child(panel.Panel(
        text="SELECTION DETAILS",
        left=0,
        top=0,
        width=280,
        height=240,
    ))
    world.add_child(panel.Panel(
        text="BUILD QUEUE",
        left=0,
        top=240,
        width=280,
        height=240,
    ))

    b = base.Base(starting_spice=1)

    tile_grid.get_tile(0, 0).add_child(b)
    tile_grid.get_tile(0, 0).add_child(builder.Builder(b))

    clock = pygame.time.Clock()

    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption(WINDOW_CAPTION)
    # pygame.display.set_icon(None) TODO set icon

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
