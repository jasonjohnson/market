import pygame

from . import entity, sprite


class Panel(entity.Entity):
    def __init__(self, text, left, top, width, height):
        super().__init__(left=left, top=top)
