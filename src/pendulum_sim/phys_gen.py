import time
import itertools
from math import *


def gen_pendulum_physics(dt, theta0, theta_dot0, m, g, l):
    a = float(-m * g * l)
    b = float(m * l * l)
    # initialize generalized coordinates
    q = theta0
    p = b * theta_dot0
    while True:
        # Update using Heun's Method
        q_dot1 = p / b
        p_dot1 = a * sin(q)
        q_dot2 = (p + dt * p_dot1) / b
        p_dot2 = a * sin(q + dt * q_dot1)
        q += dt / 2.0 * (q_dot1 + q_dot2)
        p += dt / 2.0 * (p_dot1 + p_dot2)
        yield q


# TODO: add a real-time delay to time generator for simulation
def time_flow(dt=1, start=0.0):
    for i in itertools.count():
        yield start + dt * i
        time.sleep(dt)


def func(f, i):
    for x in i:
        yield f(x)


def diff(i, dt=1.0):
    x0 = i.next()
    for x1 in i:
        yield (x1 - x0) / dt
        x0 = x1


dt = .05
start = 0
steps = 100
# t = time_flow(dt)
# x = func(lambda v: sin(v)+v,t)
# dx = diff(x,dt)
pend = gen_pendulum_physics(dt, pi / 4, 0, 1, 9.8, 1)
for val in itertools.islice(pend, start, steps):
    print val
