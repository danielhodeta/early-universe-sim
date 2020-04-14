import pygame
import random
import math

#GLOBAL PARAMETERS
PARTICLE_NUMBER = 300 #>= 3
WIDTH = 700
HEIGHT = 600
G_CONST = PARTICLE_NUMBER/150
GRAVITY = []
for i in range (PARTICLE_NUMBER):
    row = []
    for j in range (PARTICLE_NUMBER):
        row.append([0,0])
    GRAVITY.append(row)
#Set screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Particle Class 
class Particle:
    def __init__(self, type):
        self.type= type 
        self.deleted = 0 
        #Position init
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        #Color init 
        if (type == 'matter'):
            self.color = (255,255,255)
        elif (type == 'anti_matter'):
            self.color = (50,50,255)
        elif (type == 'photon'):
            self.color = (255, 166, 83)

        else:
            self.color = (0,0,0) 
        #Velocity init
        self.speedX = 0#random.uniform (-1,1)
        self.speedY = 0#random.uniform (-1,1)
        #Mass init
        if (type == 'photon'):
            self.mass = 0
        else:
            self.mass = 1
        self.resize()
        #Momentum init
        if (type == 'photon'): #Next step: photon has momentum
            self.p_x = 0
            self.p_y = 0
        else:
            self.p_x = self.mass * self.speedX
            self.p_y = self.mass * self.speedY
    def resize(self):
        self.size =  int(math.sqrt(3/8*math.pi*self.mass)) #3/8 as opposed to 3/4 to get orbits
    def calc_p(self):
        if (type == 'photon'): #Next step: photon has momentum
            self.p_x = 0
            self.p_y = 0
        else:
            self.p_x = self.mass * self.speedX
            self.p_y = self.mass * self.speedY
    def v_set(self, s_x, s_y):
        self.speedX = s_x
        self.speedY = s_y
        self.calc_p()
    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x),int(self.y)), self.size, self.size)
    def move(self, index):
        self.vectors = GRAVITY[index]
        for vector in self.vectors:
            M = 1 if self.mass == 0 else self.mass
            self.v_set(self.speedX+(vector[0]/M), self.speedY+(vector[1]/M))

        #attributes for no bounds
        self.x = (self.x + self.speedX)
        self.y = (self.y + self.speedY)

        #attributes for virtual torus
        # self.x = (self.x + self.speedX) % WIDTH
        # self.y = (self.y + self.speedY) % HEIGHT

        #self.y bound for bottom gravity
        # if (self.y >= HEIGHT-self.size):
        #     self.y = HEIGHT - self.size
        # else:
        #     self.y = (self.y + self.speedY)
    
    def macro_gravity(self, index, particles):
        for i in range (len(particles)):
            if i == index or self.deleted:
                continue
            dx = particles[i].x - self.x
            dy = particles[i].y - self.y
            r2 = math.pow(dx, 2) + math.pow(dy, 2)
            angle = abs(math.asin(dy/math.sqrt(r2)))

            #Collision condition
            if (r2 <= math.pow(self.size+particles[i].size, 2)):
                #Once collision, gravitational force set to 0 because we don't want it to shoot to infinity
                GRAVITY[index][i] = ([0,0])
                GRAVITY[i][index] = ([0,0])
                #make it bigger
                self.mass+= particles[i].mass
                self.resize()
                #Object comes to a halt upon collision -- momentum transfer is next step
                self.speedX = (self.p_x + particles[i].p_x)/self.mass
                self.speedY = (self.p_y + particles[i].p_y)/self.mass
                #Delete the second particle
                particles[i].pseduo_delete()
            #Normal condition
            else: 
                Force = (G_CONST * self.mass * particles[i].mass)/(r2)
                signX = 1 if dx==0 else dx/abs(dx)
                signY = 1 if dy==0 else dy/abs(dy)
                ForceX = Force*math.cos(angle)*signX
                ForceY = Force*math.sin(angle)*signY

                GRAVITY[index][i] = ([ForceX, ForceY])
                GRAVITY[i][index] = ([ForceX, ForceY])
    def pseduo_delete (self):
        self.mass = 0
        self.v_set(0,0)
        self.color = (0,0,0)
        self.size = 0
        self.deleted = 1
        


def createParticles(matter_flag, anti_matter_flag, photon_flag):
    particles = []
    ## Create particles
    for n in range(int(PARTICLE_NUMBER/3)):
        if matter_flag:
            particle = Particle("matter")
            particles.append(particle)
        if anti_matter_flag:
            particle = Particle("anti_matter")
            particles.append(particle)
        if photon_flag:
            particle = Particle("photon")
            particles.append(particle)

    return particles
    
def main():
    #Set Title and Icon
    pygame.display.set_caption('Early Universe Simulator')
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon) 

    particles = createParticles(1,0,0)

    #Simulation loop
    running = True
    while running:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #Display particles
        for i in range(len(particles)):
            particles[i].macro_gravity(i, particles)
            particles[i].move(i)
            particles[i].display()
        
        pygame.display.update()

if __name__ == "__main__":
    main()