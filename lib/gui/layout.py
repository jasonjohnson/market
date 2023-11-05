from lib.core import entity


class VLayout(entity.Entity):
    def __init__(self, left=0, top=0, padding=2):
        super().__init__(left=left, top=top)
        self.padding = padding
        self.width = 0
        self.height = 0
        self.elements = []

    def add(self, element):
        self.elements.append(element)
        self.add_child(element)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def update(self, _delta):
        top_offset = 0

        for element in self.elements:
            width = element.get_width()
            height = element.get_height()

            element.set_top(top_offset)
            top_offset += height + self.padding

            if width > self.width:
                self.width = width

            if height > self.height:
                self.height = height


class HLayout(entity.Entity):
    def __init__(self, left=0, top=0, padding=2):
        super().__init__(left=left, top=top)
        self.padding = padding
        self.width = 0
        self.height = 0
        self.elements = []

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def add(self, element):
        self.elements.append(element)
        self.add_child(element)

    def update(self, _delta):
        left_offset = 0

        for element in self.elements:
            width = element.get_width()
            height = element.get_height()

            element.set_left(left_offset)
            left_offset += width + self.padding

            if width > self.width:
                self.width = width

            if height > self.height:
                self.height = height
