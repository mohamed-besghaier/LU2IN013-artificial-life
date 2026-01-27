#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Calipsomulator - a simple CA and Agent-based simulator
# 2026, nb@su
# 
# GUI: curseur, z, shift+z, d, shift+d, reset, shift-reset
#

import matplotlib.pyplot as plt
import random
import numpy as np
from numba import njit
import csv
import calipsolib

# =-=-= Defining cell types

EMPTY = 0
TREE = 1
FIRE = 2
ASH = 3

colors = {
    EMPTY: (255, 255, 255),
    TREE:  (40, 200, 40),
    FIRE:  (255, 40, 40),
    ASH: (0, 0, 0)
}

# global variables

iteration = 1
total_trees_start = 0

# creation csv file

file = open('trees.csv', mode='w')
file.close()

# =-=-= simulation parameters

params = {
    "density": 0.50,
}

# =-=-= user-defined agents

def make_agents(params): # DO NOTHING
    return []

# =-=-= user-defined callular automata

# Check the neighbors of a grid

def check_FIRE (grid, x, y, dx, dy) :
    if grid[(x-1)%dx, y] == FIRE : return True

    if grid[(x+1)%dx, y] == FIRE : return True

    if grid[x, (y-1)%dy] == FIRE : return True

    if grid[x, (y+1)%dy] == FIRE : return True 

    if grid[(x-1)%dx, (y-1)%dy] == FIRE : return True

    if grid[(x-1)%dx, (y+1)%dy] == FIRE : return True

    if grid[(x+1)%dx, (y-1)%dy] == FIRE : return True

    if grid[(x+1)%dx, (y+1)%dy] == FIRE : return True

    return False

# Initialising the simulation

def init_simulation(params):
    global total_trees_start
    
    density = params["density"]
    dx = params["dx"]
    dy = params["dy"]

    grid = np.zeros((dx, dy), dtype=np.uint8)
    newgrid = np.empty((dx, dy), dtype=np.uint8)

    for x in range (dx) :
        for y in range (dy) :
            if random.random() < density :
                grid[x,y] = TREE
    
    grid[dx // 2, dy // 2] = FIRE
    
    total_trees_start = np.sum(grid == TREE)

    return grid, newgrid


# Live simulation

#@njit(cache=True)
def ca_step(grid, newgrid):
    global iteration, total_trees_start
        
    dx, dy = grid.shape

    for x in range(dx):
        for y in range(dy):
            if grid[x, y] == ASH:
                newgrid[x, y] = EMPTY
            elif grid[x, y] == FIRE:
                newgrid[x, y] = ASH
            elif grid[x, y] == TREE:
                if check_FIRE(grid, x, y, dx, dy):
                    newgrid[x, y] = FIRE
                else:
                    newgrid[x, y] = TREE
            else:
                newgrid[x, y] = EMPTY
            
            # p1 is the probability the tree burns
            # p2 is the probability that a new tree grows
            
            if iteration > 70 :
                p1 = random.random()
                p2 = random.random()
            
                if p1 < 0.002 :
                    if newgrid[x,y] == TREE : newgrid[x,y] = FIRE
            
                if p2 < 0.006 : 
                    if newgrid[x,y] == EMPTY : newgrid[x,y] = TREE
                    
    # Save updated tree fraction
    
    trees_fraction = np.sum(newgrid == TREE)/total_trees_start
    with open("trees.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([iteration, trees_fraction])
            
    iteration += 1

# =-=-= run

if __name__ == "__main__":
    calipsolib.run(
        params=params, # user-defined
        init_simulation=init_simulation, # user-defined
        ca_step=ca_step, # user-defined
        make_agents=make_agents, # user-defined
        colors=colors,
        dx=100, # CA width
        dy=100, # CA height
        display_dx=800,
        display_dy=800,
        title="Forest Fire CA", 
        verbose=True, # display stuff (can be used by user)
        fps=60 # steps per seconds (default: 60)
    )
