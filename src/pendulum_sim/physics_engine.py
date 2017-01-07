###############################################################################

"""
Code based on Gist found here:
by Craig Wm. Versek (cerca 2008)

desc: A simulation of a simple circular physical pendulum in a Lab
auth: Geoffrey Negiar
"""

###############################################################################
from __future__ import division, print_function

from math import atan2

import numpy as np
import pygame
import pygame.surfarray

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
    def __init__(self, m, l, pivot_pos=SCREEN_CENTER, theta0=np.pi / 2, radius=50, theta_dot0=0, restitution=1,
                 lab=Lab(),
                 dt=0.01):
        pygame.sprite.Sprite.__init__(self)
        self.lab = lab
        # Position from top-left of SCREEN to pendulum pivot
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
        self.pivot_center = (self.rect.width // 2, self.rect.height // 2)
        self.m_X = int(self.l * np.sin(theta0) + self.pivot_center[0])
        self.m_Y = int(self.l * np.cos(theta0) + self.pivot_center[1])
        self.m_rect = None
        self.pivot_rect = None

        self.m_pos_hist = np.zeros((0, 2))
        self.pivot_pos_hist = np.array(self.pivot_center)

        self._render()

    def _render(self):
        # clear background
        self.image.fill(COLOR['white'])
        m_pos = (self.m_X, self.m_Y)
        # draw tether
        pygame.draw.aaline(self.image, COLOR['black'], self.pivot_center, m_pos, True)
        # draw the mass
        # self.m_rect = pygame.draw.circle(self.image, COLOR['blue'], m_pos, self.radius, 0)
        self.m_rect = pygame.draw.circle(self.image, COLOR['blue'], m_pos, self.radius, 0)
        self.pivot_rect = pygame.draw.circle(self.image, COLOR['black'], self.pivot_center, 5, 0)

        xm, ym = self.m_rect.topleft
        xp, yp = self.pivot_rect.topleft
        x2, y2 = self.rect.topleft
        # make the reference absolute
        self.m_rect.topleft = (xm + x2, ym + y2)  # make the reference absolute
        self.pivot_rect.topleft = (xp + x2, yp + y2)

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
            yield (q, q_dot(p))

    def bounce(self, q, q_dot_val):
        width = self.rect.width
        height = self.rect.height
        sg = np.sign(q_dot_val)
        if self.pivot_center[0] + self.l * np.sin(self.theta) < self.radius:
            # bounce left
            self.theta = np.arcsin((self.radius - self.pivot_center[0]) / self.l)
            if np.abs(q) >= np.pi / 2:
                self.theta = np.pi - self.theta
            print(self.theta)
            self.theta_dot = -self.restitution * q_dot_val
            self.simulator = self.simulate()
        elif width - self.pivot_center[0] < self.l * np.sin(self.theta) + self.radius:
            # bounce right
            self.theta = np.arcsin((width - self.pivot_center[0] - self.radius) / self.l)
            if np.abs(q) >= np.pi / 2:
                self.theta = np.pi - self.theta
            self.theta_dot = -self.restitution * q_dot_val
            self.simulator = self.simulate()
        elif self.pivot_center[1] + self.l * np.cos(self.theta) < self.radius:
            # bounce up
            self.theta = - sg * np.arccos((self.radius - self.pivot_center[1]) / self.l)
            self.theta_dot = -self.restitution * q_dot_val
            self.simulator = self.simulate()
        elif height - self.pivot_center[1] < self.l * np.cos(self.theta) + self.radius:
            # bounce down
            self.theta = - sg * np.arccos((height - self.pivot_center[1] - self.radius) / self.l)
            self.theta_dot = -self.restitution * q_dot_val
            self.simulator = self.simulate()
        else:
            self.theta = q
            self.theta_dot = q_dot_val

    def update(self):
        q, q_dot = self.simulator.next()
        self.bounce(q, q_dot)
        X = int(self.l * np.sin(self.theta))
        Y = int(self.l * np.cos(self.theta))

        self.m_X = X + self.pivot_center[0]
        self.m_Y = Y + self.pivot_center[1]
        self.m_pos_hist = np.vstack((self.m_pos_hist, (self.m_X, self.m_Y)))
        self._render()

    def update_held(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if self.held == 'mass':
            self.m_X = mouse_x - self.lever_x - self.m_rect.width // 2
            self.m_Y = mouse_y - self.lever_y - self.m_rect.height // 2
        elif self.held == 'pivot':
            self.pivot_center = (mouse_x - self.lever_x - self.m_rect.width // 2,
                                 mouse_y - self.lever_y - self.m_rect.height // 2)
        self.l = np.sqrt((self.m_X - self.pivot_center[0]) ** 2 + (self.m_Y - self.pivot_center[1]) ** 2)
        # calculate the new parameters
        self.theta = atan2(self.m_X - self.pivot_center[0], self.m_Y - self.pivot_center[1])
        self._render()

    def grab_mass(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        m_x, m_y = self.m_rect.center
        self.held = 'mass'
        self.lever_x = mouse_x - m_x
        self.lever_y = mouse_y - m_y
        print("Grabbed the bob a vector from center ({}, {})".format(self.lever_x, self.lever_y))

    def grab_pivot(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        p_x, p_y = self.pivot_rect.center
        self.held = 'pivot'
        self.lever_x = mouse_x - p_x
        self.lever_y = mouse_y - p_y
        print("Grabbed the pivot a vector from center ({}, {})".format(self.lever_x, self.lever_y))

    def point_on_mass(self, point):
        x, y = point
        return self.m_rect.collidepoint(x, y)

    def point_on_pivot(self, point):
        x, y = point
        return self.pivot_rect.collidepoint(x, y)

    def release(self):
        # Put angle speed to zero and simulate
        # try:
        #     in_theta_dot = input("Enter a value of Theta_0.")
        #     self.theta_dot = in_theta_dot
        # except SyntaxError:
        #     self.theta_dot = 0
        self.theta_dot = 0
        self.simulator = self.simulate()
