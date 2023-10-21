from . import base, button, builder, entity, label, panel, spice, tile


class Main(entity.Entity):
    def __init__(self):
        super().__init__()

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

        self.add_child(panel_spice_field)
        self.add_child(panel_actions)
        self.add_child(panel_economy)
        self.add_child(panel.Panel(
            text="TILE DETAILS",
            left=0,
            top=0,
            width=280,
            height=240,
        ))
        self.add_child(panel.Panel(
            text="BUILD QUEUE",
            left=0,
            top=240,
            width=280,
            height=240,
        ))

        b = base.Base(starting_spice=1)

        tile_grid.get_tile(0, 0).add_child(b)
        tile_grid.get_tile(0, 0).add_child(builder.Builder(b))
