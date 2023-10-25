import collections
import json
import os

import pygame


class Sprite:
    def __init__(self, width, height, debug_border_color_override=None):
        self.surface = pygame.Surface((width, height))
        self.width = width
        self.height = height
        self.debug_fill_color = pygame.Color('white')
        self.debug_border_color = pygame.Color('magenta')
        self.debug_border_color_override = debug_border_color_override
        self.debug_border_width = 1

    def get_surface(self, debug=True):
        if debug:
            self.surface.fill(self.debug_fill_color)

            if self.debug_border_color_override:
                pygame.draw.rect(
                    surface=self.surface,
                    rect=self.surface.get_rect(),
                    color=self.debug_border_color_override,
                    width=self.debug_border_width * 2,
                )
            else:
                pygame.draw.rect(
                    surface=self.surface,
                    rect=self.surface.get_rect(),
                    color=self.debug_border_color,
                    width=self.debug_border_width,
                )

        return self.surface

    def get_global_rect(self, position):
        return self.surface.get_rect().move(position)


class SpriteSheet:
    SURFACES = collections.defaultdict(dict)

    def __init__(self, name):
        self.name = name

        if self.name not in SpriteSheet.SURFACES:
            self.load_sheet()

    def label_format(self, row, column):
        return '{}_{}'.format(row, column)

    def load_sheet(self):
        resources = os.path.join(os.path.dirname(__file__), os.pardir, 'res')

        file_image = os.path.join(resources, self.name + '.png')
        file_metadata = os.path.join(resources, self.name + '.json')

        with open(file_image) as image:
            with open(file_metadata) as metadata:
                m = json.load(metadata)
                s = pygame.image.load(image).convert_alpha()

                sheet_width, sheet_height = s.get_size()
                sprite_width = m['width']
                sprite_height = m['height']

                columns = int(sheet_height / sprite_height)
                rows = int(sheet_width / sprite_width)

                # Generate sub-surfaces and default labels for every sprite
                # in the sheet.
                for r in range(rows):
                    for c in range(columns):
                        subsurface = s.subsurface(
                            c * sprite_width,
                            r * sprite_height,
                            sprite_width,
                            sprite_height
                        )

                        SpriteSheet.SURFACES[self.name][self.label_format(r, c)] = subsurface

                # Generate custom labels based on what is supplied in the metadata,
                # and reuse the existing sub-surfaces.
                for r in range(len(m["labels"])):
                    for c in range(len(m["labels"][r])):
                        SpriteSheet.SURFACES[self.name][m['labels'][r][c]] = \
                            SpriteSheet.SURFACES[self.name][self.label_format(r, c)]

    def get_surface(self, label):
        return SpriteSheet.SURFACES[self.name][label]
