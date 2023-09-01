"""This file will import variables from sizing_parameters module
   and use them for calculation of stator geometry, this is a separate file
   of stator just for the ease of programming """

from root_folder.geometry_generator.general_sizing import sizing_parameters
from root_folder.program_data.fixed_program_data import fixed_data
import math


class StatorGeo:
    """import necessary variables from the flow channel(i.e from sizing_parameters),
          and do the required calculations"""

    bg = None
    rd = None
    nm = None
    kt = None
    bsy = None
    lg = None
    o_d = None
    slt = None
    th_tng_angl = None
    slv_thkn = None
    skw_slots = fixed_data.InitialParameters.skew_slt
    tp_shft_rd = fixed_data.InitialParameters.top_shft_rd
    slt_ara = 0.
    bck_ir_dpth = 0.
    inr_dmtr = 0.
    shnk_len = 0.
    tng_dpth = 0.
    tth_wdth = 0.
    tth_gp_angl = 0.
    tng_an_ln = 0.

    def calculate(self):
        """Doing the required calculation"""
        self.bck_ir_dpth = (3.141592 * self.rd * self.bg) / (2 * self.nm * self.kt * self.bsy)
        self.inr_dmtr = (self.rd + 2 * self.lg)
        self.tth_gp_angl = (360 / self.slt) * 0.08  # in degrees , must be converted to radians for arc length
        # calculation wherever required

        self.tth_wdth = (3.141592 * self.rd * self.bg) / (self.slt * self.kt * self.bsy)
        z = ((0.11 / 2) * self.o_d) - (0.11 * self.bck_ir_dpth) + self.inr_dmtr
        a = ((2 * 3.141592) - (self.slt * (3.141592 / 180) * self.tth_gp_angl)) / 1.11
        b = self.slt * self.tth_wdth
        sci = (2 * self.slt) / math.tan((3.141592 / 180) * self.th_tng_angl)
        self.tng_an_ln = ((z * a) - b) / (sci - (1.11 * a))  # this is xsin(k)

        # ******************************************************
        self.shnk_len = (((self.o_d - self.inr_dmtr) / 2) - self.bck_ir_dpth - (1.11 * self.tng_an_ln)) / 1.11
        # it includes tang depth factor
        self.tng_dpth = 0.11 * (self.shnk_len + self.tng_an_ln)

        r1 = (self.o_d / 2) - self.bck_ir_dpth
        r2 = r1 - self.shnk_len - self.tng_an_ln
        arc = ((3.141592 / 180) * ((360 / self.slt) - self.tth_gp_angl)) * ((self.inr_dmtr / 2) + self.tng_dpth)
        tth_ara = (self.shnk_len * self.tth_wdth) + ((arc + self.tth_wdth) * self.tng_an_ln)
        self.slt_ara = ((3.141592 * (r1 ** 2 - r2 ** 2)) / self.slt) - tth_ara

    def set_req_prmtr(self, args):
        """This method sets the required parameters for the current object of this class taken from Sizing class"""
        self.bg = args[0]
        self.rd = args[1]
        self.nm = args[2]
        self.kt = args[3]
        self.bsy = args[4]
        self.lg = args[5]
        self.o_d = args[6]
        self.slt = args[7]
        self.th_tng_angl = args[8]
        self.slv_thkn = args[9]

    def get_req_prmtr_wn(self):
        """This methods returns required values for further calculation"""
        return self.slt_ara


"""----------------------------------------------------------------------------------------------------"""


class StatorWinding:
    """This class is made to handle stator winding parameters"""
    s_l_f = None
    wl = None
    st_ln = None
    c_m_d = None
    nmp = None
    vln = None
    r_pm = None
    trq = None
    slts = None
    pl = None
    slts_ara = None
    n_t = fixed_data.InitialParameters.num_trn  # This is imported from initially fixed parameters and not from sizing
    cl_spn = 0
    cnd_ara = 0.
    rtd_cur = 0.
    rtd_cur_den = 0.

    def calculate(self):
        """This does the calculation for stator winding parameters"""

        self.cl_spn = int(self.slts / self.pl)
        self.cnd_ara = (self.s_l_f * self.slts_ara) / (self.n_t * self.wl)
        # a = (self.slts * self.n_t * self.wl * self.st_ln * 1000) / (self.c_m_d * self.cnd_ara)
        # b = (-1) * ((self.nmp * self.vln) / (2 ** 0.5 * 3 ** 0.5))
        # c = (2 * 3.141592 * self.r_pm * self.trq) / 60
        # self.rtd_cur = (((-1) * b) - ((b ** 2 - (4 * a * c)) ** 0.5)) / (2 * a)
        self.rtd_cur = (2 * 3.141592 * 1.414213 * 1.732050 * self.r_pm * self.trq) / (60 * 3 * 0.765 * self.vln)
        # 0.765 is taken as the initial power factor
        self.rtd_cur_den = self.rtd_cur / self.cnd_ara

    def set_req_prmtr(self, args):
        """This method sets the required parameters for the current object of this class,
        parameters are fetched from Sizing and StatorGeo class"""
        self.s_l_f = args[0]
        self.wl = args[1]
        self.st_ln = args[2]
        self.c_m_d = args[3]
        self.nmp = args[4]
        self.vln = args[5]
        self.r_pm = args[6]
        self.trq = args[7]
        self.slts = args[8]
        self.pl = args[9]
        self.slts_ara = args[10]
