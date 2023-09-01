"""importing necessary packages.
   We have used the python random module to select different values from the vectors
   that will help in population generation."""


import random


class Vectors:
    """This class handles the variables that vary over a range and helps in population generation
    of desired chromosome size"""

    num_poles = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 40, 42, 44, 46, 48, 50)
    # always in multiple of 2

    slots = (12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78
             , 81, 84, 87, 90, 93, 96, 99, 102, 105)  # should be always in
    # multiple of number of phases which is 3 here

    air_gp_thkns = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.8,
                    2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.3, 3.5, 4.0)  # in mm (milimeters)

    fill_fact = (0.40, 0.50, 0.60, 0.65, 0.70, 0.75)

    rotor_stator_rto = (0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.60, 0.61, 0.62, 0.63, 0.64, 0.65)

    torque_pu_vol = (1e-6, 1.5e-6, 2e-6, 2.5e-6, 3e-6, 3.5e-6, 4e-6, 4.5e-6, 5e-6, 5.5e-6, 6e-6, 6.5e-6, 7e-6,
                     1e-5, 1.5e-5, 2e-5, 2.5e-5, 3e-5, 3.5e-5, 4e-5, 4.5e-5, 5e-5, 5.5e-5, 6e-5, 6.5e-5, 7e-5,
                     1e-4, 1.2e-4, 1.4e-4, 1.6e-4, 1.8e-4, 2e-4, 2.2e-4, 2.4e-4, 2.5e-4)
    # The above torque pu volume offers a wide range of motor sizes around the standard sizes available in market

    """------other parameters will have to be included in further updates of the software
    from the FixedParameters class-----"""

    """Below are the methods responsible for generating initial random set for building a chromosome """

    def generate_random_set(self):

        a = random.choice(Vectors.num_poles)
        b = random.choice(Vectors.slots)
        c = random.choice(Vectors.air_gp_thkns)
        d = random.choice(Vectors.fill_fact)
        e = random.choice(Vectors.rotor_stator_rto)
        f = random.choice(Vectors.torque_pu_vol)
        temp_tup = (a, b, c, d, e, f)

        return temp_tup


