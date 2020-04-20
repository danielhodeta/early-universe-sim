import pygame
import random
import math
import sys 
import GLOBAL
from particle import Particle

def createParticles(matter_flag, anti_matter_flag, photon_flag):
    particles = []
    ## Create particles
    for n in range(int(GLOBAL.MATTER_RATIO * GLOBAL.PARTICLE_NUMBER)):
        if matter_flag:
            particle = Particle("matter")
            particles.append(particle)
    for n in range(int(GLOBAL.ANTI_MATTER_RATIO * GLOBAL.PARTICLE_NUMBER)):
        if anti_matter_flag:
            particle = Particle("anti_matter")
            particles.append(particle)
    for n in range(int(GLOBAL.PHOTON_RATIO * GLOBAL.PARTICLE_NUMBER)):
        if photon_flag:
            particle = Particle("photon")
            particles.append(particle)

    return particles
    
def main():
    #Set Title and Icon
    pygame.display.set_caption('Early Universe Simulator')
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon) 

    particles = createParticles(1,1,1)

    #Simulation loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        #Display particles
        for i in range(len(particles)):
            if (not particles[i].deleted):
                particles[i].macro_gravity(i, particles)
                particles[i].move(i)
                particles[i].display()
        pygame.display.update()
        GLOBAL.SCREEN.fill((0,0,0)) 

if __name__ == "__main__":
    main()