from . import entity

class World(entity.Entity):
    def __init__(self):
        super().__init__(left=0, top=0)
