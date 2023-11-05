import pygame

from lib.core import entity, sprite
from lib.gui import label


class Button(entity.Entity):
    def __init__(self, text, left=0, top=0, action=None):
        super().__init__(left=left, top=top)

        if not action:
            self.action = self.no_op
        else:
            self.action = action

        self.sheet = sprite.SpriteSheet('gui_debug')
        self.sheet_prefix = 'button'
        self.sheet_state = 'idle'
        self.sprites = {
            'nw': {
                'idle': None,
                'hover': None,
                'click': None,
            },
            'n': {
                'idle': None,
                'hover': None,
                'click': None,
            },
            'ne': {
                'idle': None,
                'hover': None,
                'click': None,
            },
            'e': {
                'idle': None,
                'hover': None,
                'click': None,
            },
            'c': {
                'idle': None,
                'hover': None,
                'click': None,
            },
            'w': {
                'idle': None,
                'hover': None,
                'click': None,
            },
            'sw': {
                'idle': None,
                'hover': None,
                'click': None,
            },
            's': {
                'idle': None,
                'hover': None,
                'click': None,
            },
            'se': {
                'idle': None,
                'hover': None,
                'click': None,
            },
        }

        for position in self.sprites:
            for state in self.sprites[position]:
                self.sprites[position][state] = \
                    self.sheet.get_surface('_'.join([
                        self.sheet_prefix,
                        position,
                        state
                    ]))

        self.label = label.Label(text, top=7, left=7)
        self.add_child(self.label)

    def no_op(self):
        return

    def get_width(self):
        return 7 + self.label.get_width() + 7

    def get_height(self):
        return 7 * 3

    def is_hovering(self, position):
        return pygame.Rect(
            self.get_left(),
            self.get_top(),
            self.get_width(),
            self.get_height()
        ).collidepoint(position)

    def inputs(self, events):
        for e in events:
            if e.type == pygame.MOUSEMOTION:
                if self.is_hovering(e.pos):
                    self.on_mouse_hover()
                else:
                    self.on_mouse_exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if self.is_hovering(e.pos) and e.button == 1:
                    self.on_mouse_down()
            elif e.type == pygame.MOUSEBUTTONUP:
                if self.is_hovering(e.pos) and e.button == 1:
                    self.on_mouse_up()
                    self.on_mouse_click()

    def render(self, surface):
        left = self.get_left()
        top = self.get_top()
        width = self.get_width()
        height = self.get_height()

        surface.blit(self.sprites['nw'][self.sheet_state], (left, top))
        surface.blit(self.sprites['ne'][self.sheet_state], (left + width - 7, top))
        surface.blit(self.sprites['w'][self.sheet_state], (left, top + 7))
        surface.blit(self.sprites['c'][self.sheet_state], (left + 7, top + 7))
        surface.blit(self.sprites['e'][self.sheet_state], (left + width - 7, top + 7))
        surface.blit(self.sprites['sw'][self.sheet_state], (left, top + height - 7))
        surface.blit(self.sprites['se'][self.sheet_state], (left + width - 7, top + height - 7))

        # The sections that "stretch" horizontally.
        for i in range(int((width - 14) / 7)):
            surface.blit(self.sprites['n'][self.sheet_state], (left + 7 + i * 7, top))
            surface.blit(self.sprites['s'][self.sheet_state], (left + 7 + i * 7, top + height - 7))

    def on_mouse_down(self):
        self.sheet_state = 'click'

    def on_mouse_up(self):
        self.sheet_state = 'hover'

    def on_mouse_hover(self):
        self.sheet_state = 'hover'

    def on_mouse_exit(self):
        self.sheet_state = 'idle'

    def on_mouse_click(self):
        self.action()
