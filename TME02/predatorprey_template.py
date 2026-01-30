#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Calipsomulator - a simple CA and Agent-based simulator
# 2026, nb@su
# 
# GUI: curseur, z, shift+z, d, shift+d, reset, shift-reset
#

import random
import numpy as np
import csv

try:
    from numba import njit
except ImportError:
    print ("[WARNING] Numba not available.")
    def njit(*args, **kwargs):
        def wrapper(f):
            return f
        return wrapper

import calipsolib
from calipsolib import Agent

# =-=-= simulation parameters

params = {
    "P_prey_alive" : 0.0090,
    "P_predator_alive" : 0.0033,
    "R_famine" : 600,
    "iteration" : 1,
    "iteration_reproduce" : 5,
    "iteration_trail" : 10,
    "len_agents" : 50,
    "prey_count" : 0,
    "pred_count" : 0,
    "counted_this_iteration" : False
}

# =-=-= Defining cell types

EMPTY = 0
TREE = 1
FIRE = 2
PREY_TRAIL = 3
PREDATOR_TRAIL = 4

colors_ca = {
    EMPTY: (255, 255, 255),
    TREE:  (40, 200, 40),
    FIRE:  (255, 40, 40),
    PREY_TRAIL: (224, 224, 255),
    PREDATOR_TRAIL:  (255, 224, 224),
}

# File Creation

file = open ("Prey_Count.csv", "w")
file.close ()

# =-=-= Defining agent types

PREY = 0
PREDATOR = 1

colors_agents = {
    PREY: (0, 0, 128),
    PREDATOR:  (128, 0, 0),
}

# =-=-= user-defined agents

class Predator(Agent) :    
    def __init__(self, x, y, params):
        super().__init__(x, y, "Predator", params)
        self.type = PREDATOR
        self.running = True
        self.trail = True
        self.hunger = 0

    def move(self, grid, agents):
        
        # Count the number of Preys and Predators
        if not params["counted_this_iteration"]:
            params["prey_count"] = sum(1 for a in agents if a.type == PREY and a.running)
            params["pred_count"] = sum(1 for a in agents if a.type == PREDATOR and a.running)
            params["counted_this_iteration"] = True
    
        if not self.running :
            return

        delta_x, delta_y = random.choice(
            [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        )
        self.x = (self.x + delta_x) % self.dx
        self.y = (self.y + delta_y) % self.dy

        if self.trail :
            grid[self.x, self.y] = PREDATOR_TRAIL

        # Check if a Predator ate a Prey
        ate = False
        for agent in agents:
            if agent.type == PREY and agent.running:
                if agent.x == self.x and agent.y == self.y:
                    agent.running = False
                    agent.trail = False
                    ate = True
                    self.hunger = 0
                    break

        if not ate :
            self.hunger += 1

        # Check if a Predator did not eat in R_famine days
        if self.hunger >= params["R_famine"] :
            self.running = False
            self.trail = False
            grid[self.x, self.y] = EMPTY
            return
        
        # Reproduce a Predator
        if self.running and (params["iteration"] % params["iteration_reproduce"] == 0) :
            if random.random() < params["P_predator_alive"] :
                agents.append(Predator(self.x, self.y, params))
                params["len_agents"] += 1

class Prey(Agent):
    
    def __init__(self, x, y, params):
        super().__init__(x, y, "Prey", params)
        self.type = PREY
        self.running = True
        self.trail = True

    def move(self, grid, agents):
        
        # Count the number of Preys and Predators
        if not params["counted_this_iteration"]:
            params["prey_count"] = sum(1 for a in agents if a.type == PREY and a.running)
            params["pred_count"] = sum(1 for a in agents if a.type == PREDATOR and a.running)
            params["counted_this_iteration"] = True
            
        if not self.running :
            return

        delta_x, delta_y = random.choice(
            [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        )
        self.x = (self.x + delta_x) % self.dx
        self.y = (self.y + delta_y) % self.dy

        if self.trail :
            grid[self.x, self.y] = PREY_TRAIL

        # Reproduce a Prey
        if self.running and (params["iteration"] % params["iteration_reproduce"] == 0):
            if random.random() < params["P_prey_alive"]:
                agents.append(Prey(self.x, self.y, params))
                params["len_agents"] += 1

# =-=-= make agents

def make_agents(params):
    dx = params["dx"]
    dy = params["dy"]
    Agent_List = []

    for i in range(params["len_agents"] - params["len_agents"]//3) :
        Agent_List.append(Prey(random.randint(0, dx-1), random.randint(0, dy-1), params))
        
    for i in range(params["len_agents"] - params["len_agents"]//3, params["len_agents"]) :
        Agent_List.append(Predator(random.randint(0, dx-1), random.randint(0, dy-1), params))

    return Agent_List

# =-=-= user-defined cellular automata

def init_simulation(params):
    dx = params["dx"]
    dy = params["dy"]
    
    grid = np.zeros((dx, dy), dtype=np.uint8)
    newgrid = np.empty((dx, dy), dtype=np.uint8)
    
    return grid, newgrid

# @njit(cache=True)
def ca_step(grid, newgrid):
    global params

    dx, dy = grid.shape
    
    params["counted_this_iteration"] = False

    for x in range(dx):
        for y in range(dy):
            newgrid[x,y] = grid[x,y]
            
            # Prevent the long trails
            if params["iteration"]%params["iteration_trail"] == 0 :
                if newgrid[x,y] == PREDATOR_TRAIL or newgrid[x,y] == PREY_TRAIL :
                    newgrid[x,y] = EMPTY
                    
    with open("Prey_Count.csv", "a", newline="") as file :
        writer = csv.writer(file)
        writer.writerow([params["iteration"], params["prey_count"]])
    
    params["iteration"] = params["iteration"] + 1

# =-=-= run

if __name__ == "__main__":
    calipsolib.run (
        params=params, # user-defined
        init_simulation=init_simulation, # user-defined
        ca_step=ca_step, # user-defined
        make_agents=make_agents, # user-defined
        colors_ca=colors_ca,
        colors_agents=colors_agents,
        dx=80, # CA width
        dy=80, # CA height
        display_dx=800,
        display_dy=800,
        title="Predator-Prey (template)", 
        verbose=False, # display stuff (can be used by user)
        fps=60 # steps per seconds (default: 60)
    )
