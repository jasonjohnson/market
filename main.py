import collections
import pprint
import random
import time

class Entity(object):
    BUS = collections.defaultdict(list)

    def __init__(self):
        self.parent = None
        self.children = []

    def get_parent(self):
        return self.parent

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child):
        self.children.remove(child)

    def get_children(self):
        return self.children
    
    def get_siblings(self):
        if not self.parent:
            return []
        # TODO: this needs to filter out "self" without modifying the
        #   list of children.
        return self.parent.get_children()

    def emit(self, signal, *args, **kwargs):
        for receiver in Entity.BUS[signal]:
            receiver(*args, **kwargs)

    def subscribe(self, signal, receiver):
        Entity.BUS[signal].append(receiver)

    def update(self, delta):
        """Called once every iteration of the game loop."""
        raise NotImplementedError

class TileGrid(Entity):
    def __init__(self, rows, columns):
        super().__init__()
        self.tiles = []
        self.grid = []
        self.generate(rows, columns)
        self.link()

        for tile in self.tiles:
            self.add_child(tile)
    
    def get_tile(self, row, column):
        return self.grid[row][column]
    
    def get_random_tile(self):
        return random.choice(self.tiles)

    def generate(self, rows, columns):
        """Generate a 2-dimensional grid of tiles."""
        for r in range(rows):
            row = []
            for c in range(columns):
                tile = Tile()
                row.append(tile)

                # Build a list of all tiles. Helps when we need
                # to get a random tile and don't care where it is.
                self.tiles.append(tile)

            # Build the grid. Same tile references, just in a row
            # and column structure.
            self.grid.append(row)

    def link(self):
        """Link each tile in the tile grid to its neighbor to the north, south,
        east and west."""
        # Link each row east-to-west, bi-directionally.
        for row in self.grid:
            previous = None
            for i, tile in enumerate(row):
                tile.west = previous

                if i == len(row) - 1:
                    break

                tile.east = row[i + 1]
                previous = tile

        # Link each tile in a row north-to-south, bi-directionally.
        for i, row in enumerate(self.grid):
            for j, tile in enumerate(row):
                if i != 0:
                    tile.north = self.grid[i - 1][j]

                if i != len(self.grid) - 1:
                    tile.south = self.grid[i + 1][j]

    def update(self, delta):
        pass

class Tile(Entity):
    def __init__(self):
        super().__init__()
        self.north = None
        self.south = None
        self.east = None
        self.west = None

    def get_neighbor_tiles(self):
        return list(filter(None, [self.north, self.south, self.east, self.west]))

    def update(self, delta):
        pass

    def render(self):
        content = "".join(map(str, self.get_children()))
        print("[%s]" % content.rjust(5), end="")

class WorkerSpawner(Entity):
    def __init__(self, tile_grid, max_workers):
        super().__init__()
        self.tile_grid = tile_grid
        self.max_workers = max_workers
        self.workers = []

    def update(self, delta):
        if len(self.workers) == self.max_workers:
            return

        worker = Worker()

        tile = tile_grid.get_random_tile()
        tile.add_child(worker)

        self.workers.append(worker)

class ResourceSpawner(Entity):
    def __init__(self, tile_grid, max_resources):
        super().__init__()
        self.tile_grid = tile_grid
        self.max_resources = max_resources
        self.resources = []

    def update(self, delta):
        if len(self.resources) == self.max_resources:
            return

        resource = Resource()

        tile = tile_grid.get_random_tile()
        tile.add_child(resource)

        self.resources.append(resource)

class World(Entity):
    def __init__(self, tile_grid, resource_spawner, worker_spawner):
        super().__init__()

        self.tile_grid = tile_grid
        self.resource_spawner = resource_spawner
        self.worker_spawner = worker_spawner

        self.add_child(tile_grid)
        self.add_child(resource_spawner)
        self.add_child(worker_spawner)

    def update(self, delta):
        pass

class Resource(Entity):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "R"

    def update(self, delta):
        pass

class Worker(Entity):
    """
    Workers can
        Be incentivized to attack competing workers
        Be incentivized to find resources of a type
        Be told where things are
        Be hired
        Hold resources
        Deposit resources
        Occupy tiles
        Have its vision enhanced
        Make value-based decisions
        Make preservation-based decisions (if its under attack)
        Die
        Steal things
    """
    def __init__(self):
        super().__init__()
        self.choices = [
            self.move,
        ]

    def __repr__(self):
        return "W"

    def move(self):
        tile = self.get_parent()
        tiles = tile.get_neighbor_tiles()

        tile.remove_child(self)

        random.choice(tiles).add_child(self)

    def update(self, delta):
        random.choice(self.choices)()

def gather_entities(root_entity):
    entities = [root_entity]

    for entity in entities:
        entities.extend(entity.get_children())

    return entities

if __name__ == "__main__":
    # A simulation. You can make decisions which influence
    # the simulation, but you cannot interact directly with
    # any of the simulated items.
    #
    # A simulation with bottlenecks. Your decisions may fix
    # the current bottleneck in the simulation, but there will
    # always be a new bottleneck.
    #
    # A simulation which can deplete your resources. Your
    # decisions may deplete your resources. If your resources
    # reach zero, you lose.
    #
    # A simulation which has no end. Your decisions may increase
    # your resources. There is no maximum. There is no win condition,
    # only survival and accumulation of resources.
    #
    # A simulation has:
    #   Universe - the container of the entire simulation
    #   Space - the presense of things
    #   Time - the passage of time
    #   Agents - temporal entities which can be influenced
    #   Resources - permanent entities which can be traded, transmuted
    #   Environment - conditions which influence agents and resources
    #
    #   Currency
    #   Soil
    #   Minerals
    #   Metals
    #   Weather
    #
    #   What is the span of control?
    #   What are the ways in which a simulation participant can
    #   interact to gain resources?
    #
    #   Lets start with something simple:
    #       A 2d plane
    #       A few resources of different values
    #       Hire agents to farm resources, and return them to a location for
    #           some amount of currency.
    #       Bottleneck: the resources respawn slowly, the distance between
    #           the resources and the deposit. Continuing to pay the worker
    #           will eventually result in losing the game.

    tile_grid = TileGrid(10, 10)

    world = World(
        tile_grid=tile_grid,
        resource_spawner=ResourceSpawner(tile_grid, 10),
        worker_spawner=WorkerSpawner(tile_grid, 2),
    )

    world_tick = 1

    while True:
        # Let one second of wall time pass. At some point we can
        # make this dymaic.
        time.sleep(world_tick)

        # Gathering this each time seems expensive, but it is the
        # most obvious way I can think of to keep the entity list
        # fresh (in case some are added/removed at run-time).
        entities = gather_entities(world)
        for entity in entities:
            entity.update(world_tick)

        print("=" * 70)

        for row in world.tile_grid.grid:
            for tile in row:
                tile.render()
            print("")
