from __future__ import division, print_function
import numpy as np


class SimplePendulum(object):
    def __init__(self, length, mass, room_width, position=None, radius=1, bounce=1):
        self.length = length
        self.mass = mass
        self.room_width = room_width
        if position is None:
            self.position = room_width / 2
        self.position = position
        self.radius = radius
        self.bounce = bounce


    def simulate_next_position(self, ):