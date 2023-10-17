## Market: a simulation game of unknown scope.

#### Theme

The spice must flow.

#### Winning

* Meet the demand of the spice market for 1 full year.

#### Ideas

* Harvest, transport, and protect enough spice to the market to meet demand
* Construction cost (time and spice)
* Upkeep cost (spice)
* Simple automatons (ex: harvester, builder, courier, etc.)
* Theoretically infinite spice field

#### Units

* **Builder**: wander away from its spawn base, build a new base, and self-destruct
* **Harvester**: wander around, gather spice, deposit spice at spawn base

#### Gameplay

![Market Gameplay as of October 2023](doc/screenshots/2023_10_14-progress.gif)

#### Pointers

* [main.py](main.py): game entry point
* [lib/automaton.py](lib/automaton.py): finite state machine class
  * [lib/builder.py](lib/builder.py): Builder unit
  * [lib/harvester.py](lib/harvester.py): Harvester unit
* [lib/entity.py](lib/entity.py): entity class, basis of the scene graph
* [lib/sprite.py](lib/sprite.py): sprite class
* [TODO.txt](TODO.txt): do, doing, done and dumped
