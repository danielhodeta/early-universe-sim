# Early Universe Simulator

This is a simulation of the interaction between matter, antimatter and photons. It hopes to recreate a very basic image of the early universe in an attempt to understand the relative densities of matter, antimatter and photons needed for the current matter dominated universe to develop.

Usage:

  `python uni-sim.py`

**Note**: uni-sim.py will create a configuration file named *sim_config.txt* in it's current directory. This file will have all user configurable parameters and flags. Each of these parameters and flags (and their default values) will be explained below.

Requirements:

  - `python 3` : [Download Here](https://www.python.org/downloads/)
  
  - `pygame` : run `pip install pygame` on terminal after installing python
  
Particle Types:

  - White  : Matter
  - Blue   : Anti-matter
  - Orange : Photon
  
**Parameters**

There are 6 user configurable parameters

*PARTICLE_NUMBER*

Type: int

`PARTICLE_NUMBER` dictates the number of particles being simulated. 50 is the default and recommended value for this parameter but any integer number is acceptable. It is worth noting that the window size is proportional to the value of `PARTICLE_NUMBER`. However, it will never fall below 450x300 and go above 1000x700.

*MATTER_RATIO*

Type: float

`MATTER_RATIO` is the fraction of `PARTICLE_NUMBER` particles that the user wants to be simulated as matter. The default value of 0.3 (or 1/3 to be exact) for an even split between matter, anti matter and photons.

*ANTI_MATTER_RATIO*

Type: float

`ANTI_MATTER_RATIO` is the fraction of `PARTICLE_NUMBER` particles that the user wants to be simulated as anti_matter. The default value of 0.3 (or 1/3 to be exact) for an even split between matter, anti matter and photons.

*PHOTON_RATIO*

Type: float

`PHOTON_RATIO` is the fraction of `PARTICLE_NUMBER` particles that the user wants to be simulated as photons. The default value of 0.3 (or 1/3 to be exact) for an even split between matter, anti matter and photons.

  *Note: The sum of `MATTER_RATIO`, `ANTI_MATTER_RATIO` and `PHOTON_RATIO` must be at most 1*

*PAIR_PRODUCTION_PROB*

Type: float

`PAIR_PRODUCTION_PROB` is a float between 0 and 1 that dictates the probability of a matter-antimatter pair being produced when two photons collide. The default value is 0.01 (1%)

  *Note: `PAIR_PRODUCTION_PROB` must be at most 1*

*GRAVITY_FACTOR*

Type: float

`GRAVITY_FACTOR` is any float and will determine the strength of the gravitational attraction between particles of mass. The default value is 1, and represents attractions under normal conditions.

  *Note: `GRAVITY_FACTOR` must be at least 0*

**Flags**

*ZERO_INITIAL_BARYON_SPEED*

  If `ZERO_INITIAL_BARYON_SPEED` is set to 1, when the simulation starts each matter/anti_matter particle will be stationary as opposed to having some random velocity. It is set to 0 by default.

*SPHERICAL_UNIVERSE*

  If `SPHERICAL_UNIVERSE` is set to 1, the universe simulated will be spherical. This means the simulation screen display is all there is to the universe. In other words, when a particle leaves the screen on one side, it will reappear on the other side. Gravity is also not bound by the boundaries of the screen. In practice, this mean particles on opposite sides of the scren will affect eachother strongly because they are close to eachother on the "other side" of the sphere. Another implication is that all particles in the universe will always be displayed on screen. If the flag is set to 0, the screen will only represent a small porition of a larger universe, i.e. when particles move out of the screen, they will not come back unless they're attracted back by a heavier particle. This flag is set to 1 by default.


    
