import collections
import pprint
import random
import time

# Need some infrastructure to scale this
# World == Scene
# World must contain objects. Scene graph? Parent/child?
# Must be able to emit and receive signals
#   Ex: when a resource is collected
#   Ex: when a worker moves
# Every entity has:
#   One parent
#   Many children
# Every entity can:
#   Emit signals w/ parameters
#   Subscribe to signals and receive parameters

class Entity(object):
    BUS = collections.defaultdict(list)

    def __init__(self):
        self.parent = None
        self.children = []

    def get_parent(self):
        return self.parent

    def add_child(self, child):
        # Add events? "on-added"
        child.parent = self
        self.children.append(child)

    def get_children(self):
        return self.children
    
    def get_siblings(self):
        if not self.parent:
            return []
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
        print("TileGrid::update(%d)" % delta)

class Tile(Entity):
    def __init__(self):
        super().__init__()
        self.north = None
        self.south = None
        self.east = None
        self.west = None

class World(Entity):
    def __init__(self):
        super().__init__()

        self.ticks = 0
        self.rows = 10
        self.columns = 10
        self.grid = []
        self.tiles = []
        self.resources = []
        self.workers = []

    def add_resource(self, resource):
        self.resources.append(resource)

    def add_worker(self, worker):
        # Inventory of all workers. The worker object should
        # probably be attached directly to a "Tile" object.
        self.workers.append(worker)

        # When added, we need a starting point.
        self.tiles[worker.row][worker.column] = 'w'

    def get_empty_tiles(self, quantity):
        tiles = []

        while len(tiles) < quantity:
            r_row = random.randint(0, self.rows - 1)
            r_column = random.randint(0, self.columns - 1)

            tile = (r_row, r_column)

            if not self.tiles[r_row][r_column] and tile not in tiles:
                tiles.append((r_row, r_column))

        return tiles

    def update(self, delta):
        # Every update, make sure we have the right number of
        # resources on tiles.
        for resource in self.resources:
            tiles_needed = resource.quantity - resource.spawned
            tiles = self.get_empty_tiles(tiles_needed)

            for (row, column) in tiles:
                self.tiles[row][column] = 'r'
                resource.spawned += 1

        # Every update, look around.
        for worker in self.workers:
            tiles = []

            if worker.row > 0:
                tiles.append((worker.row - 1, worker.column))
            
            if worker.row < self.rows - 1:
                tiles.append((worker.row + 1, worker.column))

            if worker.column > 0:
                tiles.append((worker.row, worker.column - 1))

            if worker.column < self.columns - 1:
                tiles.append((worker.row, worker.column + 1))

            row, column = random.choice(tiles)

            # Vacate the current position
            self.tiles[worker.row][worker.column] = None

            worker.row = row
            worker.column = column

            if self.tiles[worker.row][worker.column] == 'r':
                worker.collected += 1

            # Populate the new position
            self.tiles[worker.row][worker.column] = 'w'

        self.ticks += 1

        print("World Ticks: %d" % self.ticks)
        #print("Worker Collection: %d" % self.workers[0].collected)

        pprint.pprint(self.tiles)




# Make the Resource a subclass of Entity...
# class Resource(object):
#     def __init__(self, quantity):
#         self.quantity = quantity
#         self.spawned = 0

class Resource(Entity):
    def __init__(self):
        super().__init__()
        print("resource:init()")
        self.quantity = 10
        self.spawned = 0

    def update(self, delta):
        print("resource::update()")

# How much does the worker know about the world?
# Does it know where it is?
class Worker(Entity):
    def __init__(self):
        super().__init__()

        self.row = 0
        self.column = 0
        self.collected = 0
        # Can be incentivized to attack competing workers
        # Can be incentivized to find resources of a type
        # Can hold resources
        # Can deposit resources
        # Can occupy tiles
        # Can have its vision enhanced
        # Can make value-based decisions
        # Can make preservation-based decisions (if its under attack)
        # Can die
        # Can steal things from its employer
        # Can be told where things are (like depositories)
    
    def update(self, delta):
        pass

class Player(object):
    def __init__(self, currency):
        self.currency = currency

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
    world = World()
    world_tick = 1

    tile_grid = TileGrid(10, 10)

    world.add_child(tile_grid)

    #world.add_resource(resource)
    #world.add_worker(worker)

    # Worker looks around
    # Worker decides to move in a direction

    # Demand for a resource must exist. That demand can fluctuate.

    # Add a player to the world.
    # Add resources to the world which spawn at specific places.
    # Add hirable agents to the world.

    # World
    # - TileGrid
    #   - Tiles (linked N/S/E/W to each other)
    #       - per Tile
    #           - Workers (automoton)
    #               get parent, expect it to be a Tile
    #               gather information about surroundings
    #               make a decision (based on probability)
    #               take action
    #           - Resources (finite)
    # update
    # render

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
