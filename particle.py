# Daniel Hodeta
# Early Universe Simulator
# Particle Class

import math
import random
import GLOBAL
import pygame

class Particle:
    def __init__(self, type):

        self.type= type 
        self.deleted = 0 

        #Position init
        self.x = random.randint(0, GLOBAL.WIDTH)
        self.y = random.randint(0, GLOBAL.HEIGHT)

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
        if (type != 'photon'):
            if (not GLOBAL.ZERO_INITIAL_BARYON_SPEED):
                self.speedX = random.uniform (-0.75,0.75)
                self.speedY = random.uniform (-0.75,0.75)
            else:
                self.speedX = 0
                self.speedY = 0
        else:
            self.speedX = random.uniform(-GLOBAL.LIGHT_SPEED, GLOBAL.LIGHT_SPEED)
            y_direction = (random.randrange(-1, 2, 2))
            self.speedY = y_direction * math.sqrt(math.pow(GLOBAL.LIGHT_SPEED, 2) - math.pow(self.speedX, 2))
        
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
    
    def change_mass(self, new_mass):
        self.mass = new_mass
        self.resize()

    def calc_p(self):
        if (type == 'photon'): #Next step: photon has momentum
            self.p_x = 0
            self.p_y = 0
        else:
            self.p_x = self.mass * self.speedX
            self.p_y = self.mass * self.speedY
    
    def v_set(self, s_x, s_y):
        speedVector = math.sqrt(math.pow(s_x, 2) + math.pow(s_y, 2))
        factor = 0
        if (self.type == 'photon'):
            if (speedVector == GLOBAL.LIGHT_SPEED):
                factor = 1
            else:
                factor = GLOBAL.LIGHT_SPEED / speedVector if speedVector> 0 else 0
        else:
            if (speedVector <= GLOBAL.BARYON_SPEED_MAX):
                factor = 1
            else:
                factor = GLOBAL.BARYON_SPEED_MAX/speedVector if speedVector> 0 else 0
        if (factor):
            self.speedX = s_x * factor
            self.speedY = s_y * factor
            self.calc_p()
        elif (self.type == 'photon'):
            self.speedX = random.uniform(-GLOBAL.LIGHT_SPEED, GLOBAL.LIGHT_SPEED)
            y_direction = (random.randrange(-1, 2, 2))
            self.speedY = y_direction * math.sqrt(math.pow(GLOBAL.LIGHT_SPEED, 2) - math.pow(self.speedX, 2))
            self.calc_p()
        else:
            self.speedX = 0
            self.speedY = 0
            self.calc_p()
    
    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def collision(self, particle):
        #make it bigger
        if (self.mass>particle.mass):
            self.mass+= particle.mass
            self.resize()
            #momentum transfer
            speedX = (self.p_x + particle.p_x)/self.mass
            speedY = (self.p_y + particle.p_y)/self.mass
            self.v_set(speedX, speedY)
            #Delete the second particle
            particle.pseduo_delete()
            
            return 0 #self deletion flag
        else:
            particle.mass+= self.mass
            particle.resize()
            #momentum transfer
            speedX = (self.p_x + particle.p_x)/particle.mass
            speedY = (self.p_y + particle.p_y)/particle.mass
            particle.v_set(speedX, speedY)
            #Delete the second particle
            self.pseduo_delete()

            return 1 #self deletion flag

    def make_photon(self):
        #Change mass
        self.mass = 0
        #Change type
        self.type = 'photon'
        #Change color
        self.color = (255, 166, 83)
        #Change speed
        self.v_set(self.speedX, self.speedY)            #v_set() automatically scales speedX and speedY to reach LIGHT_SPEED
        #Change size
        self.resize()
        #Calculate p
        self.calc_p()
    
    def make_matter(self):
        #Change mass
        self.mass = 1
        #Change type
        self.type = 'matter'
        #Change color
        self.color = (255, 255, 255)
        #Change speed
        self.v_set(self.speedX, self.speedY)            
        #Change size
        self.resize()
        #Calculate p
        self.calc_p()

    def make_anti_matter(self):
        #Change mass
        self.mass = 1
        #Change type
        self.type = 'anti_matter'
        #Change color
        self.color = (50,50,255)
        #Change speed
        self.v_set(self.speedX, self.speedY)            
        #Change size
        self.resize()
        #Calculate p
        self.calc_p()
    
    def add_particle(self, particles):
        particles.append(self)
        #add to GRAVITY array
        gravity_array = []
        for i in range(len(GLOBAL.GRAVITY)+1):
            gravity_array.append([0,0])
        GLOBAL.GRAVITY.append(gravity_array)

        for i in range(len(GLOBAL.GRAVITY)-1):
            GLOBAL.GRAVITY[i].append([0,0])

    def annihilation(self, particle, particles, self_i, particle_i):
        if (self.mass == 1):
            self.make_photon()
        else:
            new_particle = Particle(self.type)
            new_particle.change_mass(self.mass - 1)
            new_particle.set_pos(particle.x, particle.y)

            new_speedx = -particle.p_x/new_particle.mass
            new_speedy = -particle.p_y/new_particle.mass
            new_particle.v_set(new_speedx, new_speedy)
            self.make_photon()

            new_particle.add_particle(particles)
        
        if (particle.mass == 1):
            particle.make_photon()
        else:
            new_particle = Particle(particle.type)
            new_particle.change_mass(particle.mass - 1)
            new_particle.set_pos(self.x, self.y)

            new_speedx = -self.p_x/new_particle.mass
            new_speedy = -self.p_y/new_particle.mass
            new_particle.v_set(new_speedx, new_speedy)
            particle.make_photon()

            new_particle.add_particle(particles)

        steps = 3
        for i in range(steps):
            self.move(self_i)
            particle.move(particle_i)

    def pair_produciton(self, particle, self_i, particle_i):
        rand_num = random.random()
        if (rand_num<GLOBAL.LAMBDA):
            self.make_matter()
            particle.make_anti_matter()
            steps = 3
            for i in range(steps):
                self.move(self_i)
                particle.move(particle_i)

    def display(self):
        x_pos = int(self.x) 
        y_pos = int(self.y) 
        pygame.draw.circle(GLOBAL.SCREEN, self.color, (x_pos,y_pos), self.size, self.size)
    
    def move(self, index):
        self.vectors = GLOBAL.GRAVITY[index]
        for i in range(len(self.vectors)):
            vector = self.vectors[i]
            M = 1 if self.mass == 0 else self.mass
            self.v_set(self.speedX+(vector[0]/M), self.speedY+(vector[1]/M))
            GLOBAL.GRAVITY[index][i] = [0,0]    #resetting vectors for next calculation -- prevents deleted particles from influencing

        if (GLOBAL.SPHERICAL_UNIVERSE):
            self.x = (self.x + self.speedX) % GLOBAL.WIDTH
            self.y = (self.y + self.speedY) % GLOBAL.HEIGHT
        else:
            self.x = (self.x + self.speedX)
            self.y = (self.y + self.speedY)
    
    def macro_gravity(self, index, particles):
        if (self.deleted):
            return
        for i in range (len(particles)):
            if i == index: # don't calculate gravity on self
                continue
            elif (particles[i].deleted): #if deleted skip
                continue
                
            dx = particles[i].x - self.x
            dx_reverse = -GLOBAL.WIDTH + dx if dx > 0 else GLOBAL.WIDTH + dx 
            minX = min(abs(dx), abs(dx_reverse))
            dx = dx if (not GLOBAL.SPHERICAL_UNIVERSE) or abs(dx)==minX else dx_reverse

            dy = particles[i].y - self.y
            dy_reverse = -GLOBAL.HEIGHT + dy if dy > 0 else GLOBAL.HEIGHT + dy
            minY = min(abs(dy), abs(dy_reverse))
            dy = dy if (not GLOBAL.SPHERICAL_UNIVERSE) or abs(dy)==minY else dy_reverse

            r2 = math.pow(dx, 2) + math.pow(dy, 2)
            angle = abs(math.asin(dy/math.sqrt(r2))) if math.sqrt(r2) > 0 else math.pi/2

            #Collision condition
            if(self.type == 'photon' and particles[i].type=='photon'):
                col_threshold = 5
            elif ((self.type == 'matter' or self.type == 'anti_matter') and (self.type != particles[i].type)):
                col_threshold = math.pow(self.size+particles[i].size, 2)*3 
            else:
                col_threshold = math.pow(self.size+particles[i].size, 2)/2
        
            if (r2 <= col_threshold):
                #Once collision, gravitational force set to 0 because we don't want it to shoot to infinity
                GLOBAL.GRAVITY[index][i] = ([0,0])
                GLOBAL.GRAVITY[i][index] = ([0,0])
                if (self.type != 'photon' and particles[i].type != 'photon'):
                    if (particles[i].type == self.type):
                        if(self.collision(particles[i])):
                            return  #self has been deleted
                    else:
                        self.annihilation(particles[i], particles, index, i)
                else:
                    if (particles[i].type == self.type):
                        self.pair_produciton(particles[i], index, i)
                    else:
                        continue
            #Normal condition
            else: 
                Force = (GLOBAL.G_CONST * self.mass * particles[i].mass)/r2
                signX = 1 if dx==0 else dx/abs(dx)
                signY = 1 if dy==0 else dy/abs(dy)
                ForceX = Force*math.cos(angle)*signX
                ForceY = Force*math.sin(angle)*signY

                GLOBAL.GRAVITY[index][i] = ([ForceX, ForceY])
                GLOBAL.GRAVITY[i][index] = ([ForceX, ForceY])

    def pseduo_delete (self):
        self.type = 'deleted'
        self.mass = 0
        self.v_set(0,0)
        self.color = (0,0,0)
        self.size = 0
        self.deleted = 1
