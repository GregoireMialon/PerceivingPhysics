###############################################################################

"""
Code based on Gist found here:
by Craig Wm. Versek (cerca 2008)

desc: A simulation of a simple circular physical pendulum in a Lab
auth: Geoffrey Negiar
"""

###############################################################################
from __future__ import print_function, division
import numpy as np
import pygame
import pygame.surfarray
from math import atan2

COLOR = {'black': (0, 0, 0),
         'red': (255, 0, 0),
         'green': (0, 255, 0),
         'blue': (0, 0, 255),
         'white': (255, 255, 255)}

SCREEN_WIDTH = 800
SCREEN_HEIGHT = SCREEN_WIDTH
SCREEN_DIM = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


class Lab(object):
    def __init__(self, g=9.8, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        self.g = g
        self.width = width
        self.height = height


class SimplePendulum(pygame.sprite.Sprite):
    def __init__(self, m, l, radius, pivot_pos=SCREEN_CENTER, theta0=np.pi / 2, theta_dot0=0, restitution=1, lab=Lab(),
                 dt=0.01):
        pygame.sprite.Sprite.__init__(self)
        self.lab = lab
        # Position from top-left to pendulum pivot
        self.pivot_pos = pivot_pos
        self.m = m
        self.l = l
        self.radius = radius
        self.theta = theta0
        self.theta_dot = theta_dot0
        self.restitution = restitution
        self.dt = dt
        self.simulator = self.simulate()
        swinglength = self.l + self.radius
        # Create image the right size for the tether
        self.image = pygame.Surface((swinglength * 2, swinglength * 2)).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (pivot_pos[0] - swinglength, pivot_pos[1] - swinglength)
        self.m_X = int(self.l * np.sin(theta0) + self.rect.width // 2)
        self.m_Y = int(self.l * np.cos(theta0) + self.rect.height // 2)
        self.m_rect = None

        self._render()

    def _render(self):
        # clear background
        self.image.fill(COLOR['white'])
        m_pos = (self.m_X, self.m_Y)
        # draw tether
        pygame.draw.aaline(self.image, COLOR['black'], (self.rect.width // 2, self.rect.height // 2), m_pos, True)
        # draw the mass
        # self.m_rect = pygame.draw.circle(self.image, COLOR['blue'], m_pos, self.radius, 0)
        self.m_rect = pygame.draw.circle(self.image, COLOR['blue'], m_pos, self.radius, 0)

        x1, y1 = self.m_rect.topleft
        x2, y2 = self.rect.topleft
        # make the reference absolute
        self.m_rect.topleft = (x1 + x2, y1 + y2)  # make the reference absolute

    def simulate(self):
        """Returns a generator of next angular position, at current angle and angle speed"""
        l = self.l / 1000.0
        dt = self.dt
        m = self.m
        # agregate the physical constants
        a = 1.0 / (m * l * l)
        b = float(-m * self.lab.g * l)
        # initialize generalized coordinates
        q = self.theta
        p = self.theta_dot / a
        # this is the physics! ... Hamiltonian style
        q_dot = lambda p_arg: a * p_arg
        p_dot = lambda q_arg: b * np.sin(q_arg)
        # Integrate using Runge-Kutta 4th Order Method
        while True:
            k1 = dt * q_dot(p)
            h1 = dt * p_dot(q)
            k2 = dt * q_dot(p + h1 / 2.0)
            h2 = dt * p_dot(q + k1 / 2.0)
            k3 = dt * q_dot(p + h2 / 2.0)
            h3 = dt * p_dot(q + k2 / 2.0)
            k4 = dt * q_dot(p + h3)
            h4 = dt * p_dot(q + k3)
            q += ((k1 + k4) / 2.0 + k2 + k3) / 3.0
            p += ((h1 + h4) / 2.0 + h2 + h3) / 3.0
            p, q, q_dot_val = self.bounced(p, q, q_dot(p))
            yield (q, q_dot_val)

    def bounced(self, p, q, q_dot_val):
        width = self.rect.width
        print(width)
        print(self.l * np.sin(q))
        if width // 2 - np.abs(self.l * np.sin(q)) <= self.radius:
            q_dot_val *= -self.restitution
            p *= -self.restitution
        return p, q, q_dot_val

    def update(self):
        self.theta = self.simulator.next()[0]
        X = int(self.l * np.sin(self.theta))
        Y = int(self.l * np.cos(self.theta))

        self.m_X = X + self.rect.width // 2
        self.m_Y = Y + self.rect.height // 2
        self._render()

    def update_held(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        self.m_X = mouse_x - self.lever_x - self.m_rect.width // 2
        self.m_Y = mouse_y - self.lever_y - self.m_rect.height // 2
        self.l = np.sqrt((self.m_X - self.rect.width // 2) ** 2 + (self.m_Y - self.rect.height // 2) ** 2)
        # calculate the new parameters
        self.theta = atan2(self.m_X - self.rect.width // 2, self.m_Y - self.rect.height // 2)
        self._render()

    def grab(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        m_x, m_y = self.m_rect.center
        self.held = True
        self.lever_x = mouse_x - m_x
        self.lever_y = mouse_y - m_y
        print("Grabbed the bob a vector from center ({}, {})".format(self.lever_x, self.lever_y))

    def point_on_mass(self, point):
        x, y = point
        return self.m_rect.collidepoint(x, y)

    def release(self):
        # Put angle speed to zero and simulate
        self.theta_dot = 0
        self.simulator = self.simulate()
