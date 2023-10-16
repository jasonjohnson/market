from . import entity

class Automaton(entity.Entity):
    def __init__(self):
        super().__init__()
        self.action_interval = 0.2
        self.action_interval_wait = 0.0

    def update(self, delta):
        if self.action_interval_wait < self.action_interval:
            self.action_interval_wait += delta
            self.wait()
            return

        self.act()
        self.reset()

    def wait(self):
        pass

    def act(self):
        pass

    def reset(self):
        self.action_interval_wait = 0.0
