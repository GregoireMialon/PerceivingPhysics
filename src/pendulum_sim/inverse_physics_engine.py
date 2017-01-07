"""Using MCMC to find the physics of a video - after object recognition"""

import numpy as np
from numpy.lib.scimath import arccos
from scipy.spatial.distance import euclidean

from pendulum_sim.physics_engine import SimplePendulum
from video_processing.find_center import find_pivot


def cost(measures, simulated_measures):
    return euclidean(measures, simulated_measures)


def likelihood(measures, simulated_measures):
    return np.exp(-cost(measures, simulated_measures))


def initial_guess(f='../../data/m_hist.csv'):
    # Need more than theta_0 and theta_dot ?
    guessed_len, guessed_pivot, m_pos_hist = find_pivot(f)
    rel_pos_hist = m_pos_hist - guessed_pivot
    guessed_theta = arccos(rel_pos_hist[:, 0], rel_pos_hist[:, 1])
    guessed_theta_dot = guessed_theta[1] - guessed_theta[:-2]
    guessed_restitution = 1
    guessed_radius = 50
    # guessed_radius = 20 ball_tracking.radius TODO: implement this - but no one cares
    guessed_m = 50 # TODO : smarter guess than this
    return SimplePendulum(guessed_m, guessed_len, guessed_radius, guessed_pivot, guessed_theta[0], guessed_theta_dot[0],
                          guessed_restitution)


def update_guess():
    pass