import pygame
import numpy as np
from physics_engine import *
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, MOUSEBUTTONUP


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption('Pendulum Simulation')
    # pygame.mouse.set_visible(0)

    # Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(COLOR['black'])
    # Prepare Objects
    clock = pygame.time.Clock()
    pendulum = SimplePendulum(m=1, l=300, theta0=np.pi / 5, radius=50, pivot_pos=SCREEN_CENTER)
    free_group = pygame.sprite.RenderPlain((pendulum,))
    held_group = pygame.sprite.RenderPlain()
    # Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    while True:
        clock.tick(60)
        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                print "Mouse Button Down"
                mouse_pos = pygame.mouse.get_pos()
                for p in free_group:
                    if p.point_on_mass(mouse_pos):     # if user clicked on the bob grab it
                        p.grab(mouse_pos)
                        held_group.add(p)
                        free_group.remove(p)
            elif event.type is MOUSEBUTTONUP:
                print "Mouse Button Up"
                for p in held_group:
                    p.release()
                    free_group.add(p)
                    held_group.remove(p)
        free_group.update()
        # send the mouse position to the held bobs so we can move them
        mouse_pos = pygame.mouse.get_pos()
        for p in held_group:
            p.update_held(mouse_pos)
        screen.blit(background, (0, 0))
        free_group.draw(screen)
        held_group.draw(screen)
        # pygame.draw.circle(screen, COLOR['blue'], SCREEN_CENTER, 50, 0)
        pygame.display.flip()


if __name__ == '__main__':
    main()
