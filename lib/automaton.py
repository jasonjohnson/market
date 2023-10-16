import collections

from . import entity

class Automaton(entity.Entity):
    State = collections.namedtuple('State', [
        'on_enter',
        'on_exit',
    ])

    Transition = collections.namedtuple('Transition', [
        'state_a',
        'state_b',
        'test',
        'on_success',
        'on_failure',
    ])

    def __init__(self, action_interval=0.2):
        super().__init__()

        self.action_interval = action_interval
        self.action_interval_wait = 0.0
        self.running = False
        self.state = None
        self.states = {}
        self.transitions = collections.defaultdict(list)
        self.on_idle = lambda: None
        self.on_reset = lambda: None

    def add_state(self, state, initial=False, on_enter=None, on_exit=None):
        if initial:
            self.state = state

        if not on_enter:
            on_enter = lambda: None

        if not on_exit:
            on_exit = lambda: None

        self.states[state] = Automaton.State(on_enter, on_exit)

    def add_transition(self, state_a: str, state_b: str, test: callable, on_success=None, on_failure=None):
        if not on_success:
            on_success = lambda: None

        if not on_failure:
            on_failure = lambda: None

        self.transitions[state_a].append(Automaton.Transition(
            state_a,
            state_b,
            test,
            on_success,
            on_failure
        ))

    def set_idle(self, on_idle):
        self.on_idle = on_idle
    
    def set_reset(self, on_reset):
        self.on_reset = on_reset

    def update(self, delta):
        if self.action_interval_wait < self.action_interval:
            self.action_interval_wait += delta
            self.idle()
            return

        self.act()
        self.reset()

    def idle(self):
        self.on_idle()

    def act(self):
        transitioned = False
        transitions = self.transitions[self.state]

        for transition in transitions:
            if transition.test():
                if transitioned:
                    pass

                transition.on_success()

                self.states[transition.state_a].on_exit()
                self.states[transition.state_b].on_enter()

                self.state = transition.state_b

                transitioned = True
            else:
                transition.on_failure()

    def reset(self):
        self.action_interval_wait = 0.0
        self.on_reset()
