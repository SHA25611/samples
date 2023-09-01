class FixedParameters:
    """This class is made to handle the globally fixed parameters
    When the software version will be updated for further improvements variables from this class will
    be removed to the Vector_parameters class to increase the chromosome size"""

    num_phase = 3  # unitless
    temperature = 40  # degree celcius
    motor_aspct_rto = 1  # unitless
    rotor_lctn = "interior"  # string
    rotor_type = "Surface mounted with radial magnets"  # string
    rotor_magnet_mat = "Neodymium iron boron 48/11"  # string
    stator_type = "square"  # string
    stator_coil_mat = "100% IACS"  # string
    """Torque_pu_volume = 1e-5  # N-m per mm^3 , it has been moved to Vectors"""
    stator_flux_den = 1.2  # Tesla | This should be taken as flux density for all iron parts of stator
    rotor_flux_den = 1.2  # Tesla  | This should be taken as flux density for all iron parts of rotor
    back_emf_limt = 0.9  # unitless
    mag_air_gp_rto = 5  # unitless
    mag_cvrg = 0.6667  # unitless
    mag_per_pole = 1  # unitless
    rotor_ovrhng = 0  # mm(milimeters)
    winding_lyr = 2  # unitless
    coil_mat_cond = 5.8e7  # S/m Simens per meter
    mag_remanence = 1.39  # T (Tesla)
    rel_permeability = 1.039  # unitless
    kl = 0.9  # leakage factor for magnetic flux path (unitless)
    kr = 1.2  # reluctance factor for stampings and air (unitless)
    c_phi = 1  # concentration factor (unitless)
    stk_fact = 1  # unitless | This is the stacking factor for laminations
    pw_fact = 1  # unitless | This is the targeted power factor and will forever remain fixed


class InitialParameters:
    """This class is just made to distinguish the globally fixed parameters
       from the initially fixed parameters"""

    num_trn = 1  # unitless  +ve integer
    skew_slt = 1  # unitless +ve integer
    # where n is the index of nth harmonic : unit is electrical radians
    tang_dpth_fact = 0.11  # tang depth is initially taken to be 11% of shank length
    sleev_thckn = 0.  # it is th magnet retention sleeve thickness  | unit:- mm(millimeters)
    mag_tp_rad = 0.  # it is the tip radius to smooth the magnetic surface | unit:- mm(millimeters)
    tth_tng_angl = 30.00  # it is the initial value of tooth tang angle | unit:- degrees
    top_shft_rd = 0.02  # unit :- mm


