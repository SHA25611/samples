"""This sizing parameter class does the calculation for the initial sizing of the motor,
   by using the pre obtained variable
   from fixed data,user inputs and the vectors"""

from root_folder.program_data.fixed_program_data import fixed_data


class Sizing:
    """Here we are generating the vector  from the vector_parameters
              and using it for further calculation , as well as importing variables
              from different data classes"""

    n_p = None
    s_l = None
    a_gp = None
    f_f = None
    r_sr = None
    o_dmt = None
    vl = None
    t = None
    rpm = None
    np = fixed_data.FixedParameters.num_phase
    nt = fixed_data.InitialParameters.num_trn
    tpu = None
    mg_rem = fixed_data.FixedParameters.mag_remanence
    rel_p = fixed_data.FixedParameters.rel_permeability
    lf = fixed_data.FixedParameters.kl
    rf = fixed_data.FixedParameters.kr
    cf = fixed_data.FixedParameters.c_phi
    mg_agp_r = fixed_data.FixedParameters.mag_air_gp_rto
    kst = fixed_data.FixedParameters.stk_fact
    r_fd = fixed_data.FixedParameters.rotor_flux_den
    s_fd = fixed_data.FixedParameters.stator_flux_den
    n_wl = fixed_data.FixedParameters.winding_lyr
    cl_m_cnd = fixed_data.FixedParameters.coil_mat_cond
    mg_cvrge = fixed_data.FixedParameters.mag_cvrg
    tng_ang = fixed_data.InitialParameters.tth_tng_angl
    slv_thk = fixed_data.InitialParameters.sleev_thckn
    stk_len = 0.
    rotor_od = 0.
    Bg = 0.
    mg_tkh = 0.
    m_as_rto = 0.
    st_dm_rto = 0.

    def calculate(self):
        """Doing the required calculations"""
        self.mg_tkh = self.mg_agp_r * self.a_gp
        pc = self.mg_tkh / self.a_gp
        self.Bg = ((self.lf * self.cf) / (1 + self.rf * (self.rel_p / pc))) * self.mg_rem
        self.rotor_od = self.o_dmt * self.r_sr
        self.stk_len = (self.t / self.tpu) / ((self.rotor_od / 2) ** 2 * 3.141592)
        self.m_as_rto = self.stk_len / self.o_dmt
        self.st_dm_rto = (self.rotor_od + 2 * self.a_gp + 2 * self.slv_thk) / self.o_dmt

    def set_req_prmtr(self, args):
        """This method sets the required parameters for the current object of this class,
        parameters are fetched from Vector class and Specifications class"""
        self.n_p = args[0]
        self.s_l = args[1]
        self.a_gp = args[2]
        self.f_f = args[3]
        self.r_sr = args[4]
        self.tpu = args[5]
        self.vl = args[6]
        self.rpm = args[7]
        self.t = args[8]
        self.o_dmt = args[9]

    def get_req_prmtr_statr(self):
        """This functions returns a tuple to be used for further calculation in stator geometry"""
        return self.Bg, self.rotor_od, self.n_p, self.kst, self.s_fd, self.a_gp, self.o_dmt, self.s_l, self.tng_ang, \
               self.slv_thk


    def get_req_prmtr_wndng(self):
        """This functions returns a tuple to be used for further calculation in stator winding"""
        return self.f_f, self.n_wl, self.stk_len, self.cl_m_cnd, self.np, self.vl, self.rpm, self.t, self.s_l, self.n_p

    def get_req_prmtr_rotr(self):
        """This functions returns a tuple to be used for further calculation in rotor"""
        return self.Bg, self.kst, self.r_fd, self.n_p, self.rotor_od, self.mg_tkh, self.mg_cvrge
