import collections

def gather_entities(root_entity):
    entities = [root_entity]

    for entity in entities:
        entities.extend(entity.get_children())

    return entities

class Entity(object):
    BUS = collections.defaultdict(list)

    def __init__(self):
        self.parent = None
        self.children = []
        self.x = 0
        self.y = 0
        self.z = 0

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def remove_parent(self):
        self.parent = None

    def get_children(self):
        return self.children

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def remove_child(self, child):
        child.parent = None
        self.children.remove(child)

    def get_siblings(self):
        if not self.parent:
            return []

        # Filter "self" from the parent's children. This does not create
        # a new list or modify the underlying list. It simly returns an
        # iterator which filters out "self" (or that what it should do!)
        return filter(lambda c: c != self, self.parent.get_children())

    def add_sibling(self, sibling):
        if not self.parent:
            raise LookupError("Entity has no parent. Cannot add sibling.")
        self.parent.add_child(sibling)

    def emit(self, signal, *args, **kwargs):
        for receiver in Entity.BUS[signal]:
            receiver(*args, **kwargs)

    def subscribe(self, signal, receiver):
        Entity.BUS[signal].append(receiver)

    def inputs(self, events):
        return

    def update(self, delta):
        return

    def render(self, surface):
        return
