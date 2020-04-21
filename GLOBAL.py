#A list of all global parameters

import math
import sys
import pygame

#User inputted global variables
if (len(sys.argv)>1):
    PARTICLE_NUMBER = int(sys.argv[1]) #>= 3        User input 
    if (len(sys.argv)==5):
        MATTER_RATIO = float(sys.argv[2])
        ANTI_MATTER_RATIO = float(sys.argv[3])
        PHOTON_RATIO = float(sys.argv[4])
    else:                                           #Default params
        MATTER_RATIO = 1/3
        ANTI_MATTER_RATIO = 1/3
        PHOTON_RATIO = 1/3 
else:                                               #Default params 
    PARTICLE_NUMBER = 100
    MATTER_RATIO = 1/3
    ANTI_MATTER_RATIO = 1/3
    PHOTON_RATIO = 1/3

if (MATTER_RATIO+ANTI_MATTER_RATIO+PHOTON_RATIO > 1):
    print("Bad ratio")
    exit(1)


#Set screen height and width 
WIDTH = PARTICLE_NUMBER * 6
HEIGHT = PARTICLE_NUMBER * 6

#Gravitational constant
G_CONST = 2

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

#Pair production probability
LAMBDA = 0.1

#Set screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))