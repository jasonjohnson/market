from . import base, entity


class BudgetEnforcer(entity.Entity):
    def __init__(self):
        super().__init__()

        self.evaluation_interval = 10.0  # every 10 seconds? No idea if this is a good value.
        self.evaluation_interval_wait = 0.0

    def update(self, delta):
        if self.evaluation_interval_wait < self.evaluation_interval:
            self.evaluation_interval_wait += delta
            return

        self.evaluate()
        self.reset()

    def reset(self):
        self.evaluation_interval_wait = 0.0

    def evaluate(self):
        for b in base.Base.BASES:
            upkeep = b.compute_upkeep()

            b.debit_spice(upkeep)
            b.reduce_force()
