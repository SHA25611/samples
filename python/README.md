>**AI Based motor design software**

This software is built for initializing and optimizing the electrical design parameters of
an Electric Motor. 

Based on **4 user inputs** it generates and optimizes **38 parameters** which 
contribute towards the performance of the motor.

The software uses a cordinated map of equations to generate a pool of solutions having
a size of **1000 solutions** and then runs a fitness algorithm to evolve the most optimized
solution untill a stretch of **14 generations**.

**The Fitness Algorithm:-**
    It follows the structure of Genetic Algorithm, where new solutions are built from older 
    ones using genetic reproduction and tested for fitness as per a well defined fitness function.
    This process is repeated till we reach a saturation level having the most fittest solution.
    
**Please checkout the root_folder to view the source code of all the logical
components of the software.**
