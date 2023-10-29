### DO
- Add build queue
- Add harvester spawn sfx
- Add a game start scene
- Add a game end scene
- Add probability of units exploding (catastrophic failure, total loss of investment)
- Add probability of units breaking down (occupying a tile)
- Fix: harvesters are a little too dumb (give them short-term memory?)
- Fix: buttons aren't specialized
- Fix: Cyclic import (lib.base -> lib.harvester)
- Fix: Duplicate code (lib.button & lib.label)
- Fix: Duplicate code (lib.harvester & lib.builder "move" methods)


### DOING
- Add "spawn Builder" button


### DONE
- Add a budget entity that evaluates the budget every N seconds
- Add spice respawning rate
- Add harvester destruction based on upkeep shortfall
- Add explosion effect when harvesters die
- Add budget enforcement
- Fix: labels aren't specialized
- Fix: window icon
- Add harvester spawn button graphics (normal, hover, down)
- Add spice graphic
- Add harvester graphic
- Add base tile graphic (or a few)
- Add a background graphic
- Fix: make tile building and resource capacity-aware
- Fix: make builder and spice spawner capacity-aware
- Fix: limit tile capacity to create bottlenecks
- Fix: tile selection sprite rendering is broken
- Fix: spawning a harvester spawns one from every base
- Add tile selection
- Fix: linting
- Fix: lots of duplication of rect and rendering code in entities
- Fix: button mouse position on "up" doesn't need to be hovering
- Fix: harvester movement back to base is boring
- Fix: use the Automaton class for the Harvester
- Fix: use the Sprite class everywhere
- Fix: remove poor rect handling
- Fix: remove some unused imports
- Fix: rewrite Builder to use FSM infrastructure
- Add "tests" (simple FSM infrastructure) to the base Automaton class
- Add Builder automaton
- Add Sprite class
- Add TileSlot placeholder (need to limit tile capacity to create bottlenecks)
- Add Automaton base class, specializing Entity
- Fix: Speed up all automaton actions (1s -> 200ms)
- Fix: entities don't have a position
- Fix: harvester uses hasattr to determine if it is on a tile
- Fix: button doesn't use x, y, z and width, height correctly
- Add overall interface layout with placeholders and labels
- Add global positioning for entities
- Add button for the player to build a harvester
- Fix: main file is getting unweidly
- Fix: entity is getting unweidly (use components?)
- Fix: everything runs too fast using pygame loop
- Add inputs, update, and render functions to all entities
- Render with pygame
- Setup pygame
- Add Harvester with basic seek/collect/deposit behaviors
- Add Spice
- Add Base
- Add test discovery
- Add test runner
- Add tests for Entity (concerned about sibling behavior)
- Get basic simulation running 


### DUMP
- Capture video with pygame (low value, can only capture image of surface)
- Fix: type hinting. Will use it only when it makes sense
- Fix: padding isn't working correctly
