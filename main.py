"""Main"""

import pygame

from lib import entity, scene

WINDOW_CAPTION = "Market"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()

    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption(WINDOW_CAPTION)
    # pygame.display.set_icon(None) TODO set icon

    events = []

    # TODO enable scene switching somehow
    current_scene = scene.Main()

    while True:
        delta = clock.tick() / 1000.0
        events.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            else:
                events.append(event)

        surface.fill((255, 255, 255))

        # Gathering this each time seems expensive, but it is the
        # most obvious way I can think of to keep the entity list
        # fresh (in case some are added/removed at run-time).
        entities = entity.gather_entities(current_scene)

        for e in entities:
            e.inputs(events)

        for e in entities:
            e.update(delta)

        for e in entities:
            e.render(surface)

        pygame.display.update()
