import pygame

from . import base, entity, sprite, tile, label


class Button(entity.Entity):
    def __init__(self, text, left=0, top=0, action=None):
        super().__init__(left=left, top=top)

        if not action:
            self.action = self.no_op
        else:
            self.action = action

        self.sprites = sprite.SpriteSheet('buttons')
        self.sprite = self.sprites.get_surface('idle')

        self.label = label.Label(text, left=10, top=11)
        self.add_child(self.label)

    def no_op(self):
        return

    def is_hovering(self, position):
        return pygame.Rect(
            self.get_left(),
            self.get_top(),
            self.sprite.get_width(),
            self.sprite.get_height()
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
        surface.blit(self.sprite, self.get_position())

    def on_mouse_down(self):
        self.sprite = self.sprites.get_surface('click')

    def on_mouse_up(self):
        self.sprite = self.sprites.get_surface('hover')

    def on_mouse_hover(self):
        self.sprite = self.sprites.get_surface('hover')

    def on_mouse_exit(self):
        self.sprite = self.sprites.get_surface('idle')

    def on_mouse_click(self):
        self.action()

