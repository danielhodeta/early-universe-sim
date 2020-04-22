# Daniel Hodeta
# Early Universe Simulator
# Global Variables

import math
import sys
import pygame
import random

# == DEFAULT VALUES ==

#Parameters
PARTICLE_NUMBER=50
MATTER_RATIO=1/3
ANTI_MATTER_RATIO=1/3
PHOTON_RATIO=1/3
LAMBDA=0.01
G_CONST = 2

#Flags
ZERO_INITIAL_BARYON_SPEED=0
SPHERICAL_UNIVERSE=1

# ==                ==

#Reading values from config file

try:
    param_file = open("sim_config.txt", "r")
except FileNotFoundError:
    param_file = open("sim_config.txt", "w+")
    param_file.write("# The following are simulation input parameters.\n")
    param_file.write("# If there is no input default values will be used\n")
    param_file.write("# Remove any space between the variable names, the\n")
    param_file.write("# equal sign and the value\n\n")

    param_file.write("#parameters\n")
    param_file.write("PARTICLE_NUMBER=50\n")
    param_file.write("MATTER_RATIO=0.3\n")
    param_file.write("ANTI_MATTER_RATIO=0.3\n")
    param_file.write("PHOTON_RATIO=0.3\n")
    param_file.write("PAIR_PRODUCTION_PROB=0.01\n")
    param_file.write("GRAVITY_FACTOR=1\n\n")

    param_file.write("#flags\n")
    param_file.write("ZERO_INITIAL_BARYON_SPEED=0\n")
    param_file.write("SPHERICAL_UNIVERSE=1\n")

params = param_file.readlines()
for param in params:
    if (param[0]=='#'):
        continue
    else:
        try:
            var = param.split("=")[0]
            val = param.split("=")[1]
        except IndexError:
            continue
    
        try:
            if (var == 'PARTICLE_NUMBER'):
                PARTICLE_NUMBER = int(val)
            elif (var == 'MATTER_RATIO'):
                MATTER_RATIO = float(val)
            elif (var == 'ANTI_MATTER_RATIO'):
                ANTI_MATTER_RATIO = float(val)
            elif (var == 'PHOTON_RATIO'):
                PHOTON_RATIO = float(val)
            elif (var == 'PAIR_PRODUCTION_PROB'):   #pair production probability
                LAMBDA = float(val)
            elif (var == 'GRAVITY_FACTOR'):
                G_CONST = G_CONST * float(val)
            elif (var == 'ZERO_INITIAL_BARYON_SPEED'):
                ZERO_INITIAL_BARYON_SPEED = int(val)
            elif (var == 'SPHERICAL_UNIVERSE'):
                SPHERICAL_UNIVERSE = int(val)
        except ValueError:
            continue

param_file.close()

#Error check
if (MATTER_RATIO+ANTI_MATTER_RATIO+PHOTON_RATIO > 1):
    print("Bad ratio")
    exit(1)
if (LAMBDA > 1):
    print("Bad pair production ratio")
    exit(1)
if (G_CONST<0):
    print("Bad gravity factor")
    exit(1)


#Set screen height and width 
WIDTH = min((PARTICLE_NUMBER * 9), 1000) if PARTICLE_NUMBER > 50 else 450
HEIGHT = min ((PARTICLE_NUMBER * 6), 700) if PARTICLE_NUMBER > 50 else 300

#Gravity array for the interaction between particles
GRAVITY = []
for i in range (PARTICLE_NUMBER):
    row = []
    for j in range (PARTICLE_NUMBER):
        row.append([0,0])
    GRAVITY.append(row)

#Global speed parameters
LIGHT_SPEED = 1.5
BARYON_SPEED_MAX = 1

#Set screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))