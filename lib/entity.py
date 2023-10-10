import collections


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

    def add_sibling(self, sibling):
        if not self.parent:
            raise LookupError("Entity has no parent. Cannot add sibling.")
        self.parent.add_child(sibling)

    def remove_child(self, child):
        child.parent = None
        self.children.remove(child)

    def get_children(self):
        return self.children

    def get_siblings(self):
        if not self.parent:
            return []

        # Filter "self" from the parent's children. This does not create
        # a new list or modify the underlying list. It simly returns an
        # iterator which filters out "self" (or that what it should do!)
        return filter(lambda c: c != self, self.parent.get_children())

    def emit(self, signal, *args, **kwargs):
        for receiver in Entity.BUS[signal]:
            receiver(*args, **kwargs)

    def subscribe(self, signal, receiver):
        Entity.BUS[signal].append(receiver)

    def update(self, delta):
        """Called once every iteration of the game loop."""
        pass
