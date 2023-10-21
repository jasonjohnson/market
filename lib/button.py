import pygame

from . import base, entity, sprite, tile


class Button(entity.Entity):
    def __init__(self, text, width=200, height=20):
        super().__init__(left=10, top=10)

        self.sprite = sprite.Sprite(width, height)
        self.color = pygame.Color('magenta')
        self.font = pygame.font.Font(None, 14)
        self.text = text
        self.selected_tile: tile.Tile | None = None

        self.subscribe('change_tile_selection', self.on_change_tile_selection)

    def is_hovering(self, position):
        return self.sprite.get_global_rect(
            self.get_position()).collidepoint(position)

    def inputs(self, events):
        for e in events:
            if e.type == pygame.MOUSEMOTION:
                self.on_mouse_hover()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if self.is_hovering(e.pos) and e.button == 1:
                    self.on_mouse_down()
            elif e.type == pygame.MOUSEBUTTONUP:
                if self.is_hovering(e.pos) and e.button == 1:
                    self.on_mouse_up()
                    self.on_mouse_click()

    def render(self, surface):
        label = self.font.render(self.text, False, self.color)

        surface.blit(self.sprite.get_surface(), self.get_position())
        surface.blit(label, self.get_position())

    def on_mouse_down(self):
        pass

    def on_mouse_up(self):
        pass

    def on_mouse_hover(self):
        pass

    def on_mouse_click(self):
        if not self.selected_tile:
            return

        selected_base = self.selected_tile.get_child_of_kind(base.Base)

        if not selected_base:
            return

        selected_base.spawn_harvester()

    def on_change_tile_selection(self, selected_tile):
        self.selected_tile = selected_tile
