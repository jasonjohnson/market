from lib.core import entity, sprite


class ProgressBar(entity.Entity):
    def __init__(self, left=0, top=0, width=210, binding=None):
        super().__init__(left=left, top=top)

        self.progress = 0.5

        # TODO figure out how to inherit this from the parent
        #   so that the gui element "fills out" the space available.
        self.width = width

        self.binding = binding
        self.binding_interval = 0.5
        self.binding_timer = 0.0

        self.sheet = sprite.SpriteSheet('gui_debug')
        self.sheet_prefix = 'progress'
        self.sprites = {
            'frame': {
                'nw': None,
                'n': None,
                'ne': None,
                'w': None,
                'c': None,
                'e': None,
                'sw': None,
                's': None,
                'se': None,
            },
            'bar': {
                'nw': None,
                'n': None,
                'ne': None,
                'w': None,
                'c': None,
                'e': None,
                'sw': None,
                's': None,
                'se': None,
            }
        }

        for name in self.sprites:
            for position in self.sprites[name]:
                self.sprites[name][position] = \
                    self.sheet.get_surface('_'.join([
                        self.sheet_prefix,
                        name,
                        position
                    ]))

        import pprint
        pprint.pprint(self.sprites)

    def get_width(self):
        return self.width

    def get_height(self):
        return 7 * 3

    def set_progress(self, progress):
        self.progress = progress

    def update(self, delta):
        if not self.binding:
            return

        if self.binding_timer < self.binding_interval:
            self.binding_timer += delta
            return

        self.set_progress(self.binding())

        self.binding_timer = 0.0

    def render(self, surface):
        self.render_frame(surface)
        self.render_bar(surface)

    def render_bar(self, surface):
        left = self.get_left()
        top = self.get_top()
        width = self.get_width()
        height = self.get_height()

        # This is a tricky bit. Here's why I'm doing this:
        #   - Remove space for each end of the bar
        #   - Handle zero progress state by clamping to 0 width
        #   - Ensure the result is evenly divisible by 7 (our sprite width)
        bar_width = width - 14
        bar_width = max(0, int(self.progress * bar_width))
        bar_width = bar_width - bar_width % 7

        surface.blit(self.sprites['bar']['nw'], (left, top))
        surface.blit(self.sprites['bar']['w'], (left, top + 7))
        surface.blit(self.sprites['bar']['sw'], (left, top + height - 7))

        for i in range(int(bar_width / 7)):
            surface.blit(self.sprites['bar']['n'], (left + 7 + i * 7, top))
            surface.blit(self.sprites['bar']['c'], (left + 7 + i * 7, top + 7))
            surface.blit(self.sprites['bar']['s'], (left + 7 + i * 7, top + 14))

        surface.blit(self.sprites['bar']['ne'], (left + bar_width + 7, top))
        surface.blit(self.sprites['bar']['e'], (left + bar_width + 7, top + 7))
        surface.blit(self.sprites['bar']['se'], (left + bar_width + 7, top + height - 7))

    def render_frame(self, surface):
        left = self.get_left()
        top = self.get_top()
        width = self.get_width()
        height = self.get_height()

        surface.blit(self.sprites['frame']['nw'], (left, top))
        surface.blit(self.sprites['frame']['ne'], (left + width - 7, top))
        surface.blit(self.sprites['frame']['w'], (left, top + 7))
        surface.blit(self.sprites['frame']['e'], (left + width - 7, top + 7))
        surface.blit(self.sprites['frame']['sw'], (left, top + height - 7))
        surface.blit(self.sprites['frame']['se'], (left + width - 7, top + height - 7))

        for i in range(int((width - 14) / 7)):
            surface.blit(self.sprites['frame']['n'], (left + 7 + i * 7, top))
            surface.blit(self.sprites['frame']['c'], (left + 7 + i * 7, top + 7))
            surface.blit(self.sprites['frame']['s'], (left + 7 + i * 7, top + height - 7))