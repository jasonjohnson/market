import random

import pygame

from lib import base, budget, spice, tile
from lib.core import entity, sprite
from lib.gui import button, panel, label, layout, progress_bar


class Main(entity.Entity):
    def __init__(self):
        super().__init__()

        self.subscribe('change_tile_selection', self.handle_tile_selection)

        self.sprites = sprite.SpriteSheet('background')
        self.selected_tile = None

        tile_grid = tile.TileGrid(34, 34)
        spice_spawner = spice.SpiceSpawner(tile_grid, int((34 * 34) * 0.1))

        panel_spice_field = panel.Panel(
            text="SPICE FIELD",
            left=280,
            top=0,
            width=720,
            height=720,
        )
        panel_spice_field.add_child(tile_grid)
        panel_spice_field.add_child(spice_spawner)

        panel_actions = panel.Panel(
            text="ACTIONS",
            left=1000,
            top=0,
            width=280,
            height=360,
        )

        panel_actions.add_child(label.Label("ACTIONS", left=10, top=20))
        panel_actions.add_child(button.Button("SPAWN HARVESTER", left=10, top=30, action=self.do_spawn_harvester))
        panel_actions.add_child(button.Button("SPAWN BUILDER", left=10, top=65, action=self.do_spawn_builder))

        budget_enforcer = budget.BudgetEnforcer()

        panel_budget = panel.Panel(
            text="BUDGET",
            left=1000,
            top=360,
            width=280,
            height=360,
        )
        panel_budget.add_child(label.Label("BUDGET", left=10, top=15))
        panel_budget.add_child(budget_enforcer)

        panel_economy = panel.Panel(
            text="ECONOMY",
            left=0,
            top=480,
            width=280,
            height=240,
        )
        panel_economy.add_child(label.Label("ECONOMY", left=20, top=15))

        panel_details = panel.Panel(
            text="DETAILS",
            left=0,
            top=0,
            width=280,
            height=240,
        )
        panel_details.add_child(label.Label("SELECTION DETAILS", left=20, top=20))

        panel_queue = panel.Panel(
            text="QUEUE",
            left=0,
            top=240,
            width=280,
            height=240,
        )
        panel_queue.add_child(label.Label("SELECTION ACTIVITY QUEUE", left=20, top=15))

        self.add_child(panel_spice_field)
        self.add_child(panel_actions)
        self.add_child(panel_budget)
        self.add_child(panel_economy)
        self.add_child(panel_details)
        self.add_child(panel_queue)

        tile_grid.get_tile(
            row=random.randint(0, 33),
            column=random.randint(0, 33)
        ).add_building(base.Base(starting_spice=1))

    def handle_tile_selection(self, selected_tile):
        self.selected_tile = selected_tile

    def do_spawn_harvester(self):
        if not self.selected_tile:
            return

        selected_base = self.selected_tile.get_child_of_kind(base.Base)

        if not selected_base:
            return

        selected_base.spawn_harvester()

    def do_spawn_builder(self):
        if not self.selected_tile:
            return

        selected_base = self.selected_tile.get_child_of_kind(base.Base)

        if not selected_base:
            return

        selected_base.spawn_builder()

    def render(self, surface):
        surface.blit(self.sprites.get_surface('background'), self.get_position())


class TestGUI(entity.Entity):
    def __init__(self):
        super().__init__()

        self.sprites = sprite.SpriteSheet('gui_debug')

        self.v_layout = layout.VLayout(left=5, top=5)

        self.v_layout.add(button.Button('INCREASE LAYOUT PADDING', action=self.increase_padding))
        self.v_layout.add(button.Button('DECREASE LAYOUT PADDING', action=self.decrease_padding))
        self.v_layout.add(button.Button('A VERY VERY VERY LONG LABEL THAT TESTS THE 9-SLICE STRETCH'))
        self.v_layout.add(button.Button('$ % / - + 0 1 2 3 4'))
        self.v_layout.add(button.Button('A BUTTON WITH ARBITRARY OFFSETS'))

        self.add_child(self.v_layout)

        self.h_layout = layout.HLayout()
        self.h_layout.add(button.Button('BEEP BOOP 1'))
        self.h_layout.add(button.Button('BEEP BOOP 2'))
        self.h_layout.add(button.Button('BEEP BOOP 3'))
        self.h_layout.add(button.Button('BEEP BOOP 4'))

        self.v_layout.add(self.h_layout)
        self.v_layout.add(progress_bar.ProgressBar(binding=self.get_progress))

    def decrease_padding(self):
        self.v_layout.padding -= 1
        self.h_layout.padding -= 1

    def increase_padding(self):
        self.v_layout.padding += 1
        self.h_layout.padding += 1

    def get_progress(self):
        return random.choice([0.0, 0.1, 0.2, 1.0])

    def render(self, surface):
        surface.fill(pygame.Color('white'))
