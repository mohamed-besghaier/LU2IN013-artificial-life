#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Calipsomulator - a simple CA and Agent-based simulator
# 2026, nb@su
# 
# GUI: curseur, z, shift+z, d, shift+d, reset, shift-reset
#

import random
import numpy as np
from numba import njit

import calipsolib

# =-=-= Defining cell types

EMPTY = 0
CAR = 1

colors = {
    EMPTY: (255, 255, 255),
    CAR:  (255, 128, 128),
}

# =-=-= simulation parameters

params = {
    "density": 0.60,
}

# =-=-= user-defined agents

def make_agents(params): # DO NOTHING
    return []

# =-=-= user-defined cellular automata

def init_simulation(params):
    density = params["density"]
    dx = params["dx"]
    dy = params["dy"]

    grid = np.zeros((dx, dy), dtype=np.uint8)
    newgrid = np.empty((dx, dy), dtype=np.uint8)

    grid[dx // 2, dy // 2] = CAR

    return grid, newgrid

@njit(cache=True)
def ca_step(grid, newgrid):
    dx, dy = grid.shape
    for x in range(dx):
        newgrid[x, 0] = grid[x, 0] # simple copy of state

# =-=-= run

if __name__ == "__main__":
    calipsolib.run(
        params=params, # user-defined
        init_simulation=init_simulation, # user-defined
        ca_step=ca_step, # user-defined
        make_agents=make_agents, # user-defined
        colors=colors,
        dx=80, # CA width
        dy=1, # CA height
        display_dx=800,
        display_dy=800,
        title="Traffic Jam CA", 
        verbose=True, # display stuff (can be used by user)
        fps=5 # steps per seconds (default: 60)
    )
