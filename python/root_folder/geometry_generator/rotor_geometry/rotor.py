"""This file will import variables from sizing_parameters module
   and use them for calculation of rotor geometry, this is a separate file
   of rotor just for the ease of programming """

from root_folder.geometry_generator.general_sizing.sizing_parameters import Sizing
from root_folder.program_data.fixed_program_data import fixed_data


class RotorGeo:
    """import necessary variables from the flow channel(i.e from sizing_parameters),
          and do the required calculations"""
    bg = None  # Bg
    kst = None  # kst
    bry = None  # r_fd
    nm = None  # n_p
    dr = None  # rotor_od
    mg_tkhn = None  # mg_tkh
    mg_cvrg = None  # mg_cvrge
    slv_thkn = fixed_data.InitialParameters.sleev_thckn
    mg_tp_r = fixed_data.InitialParameters.mag_tp_rad
    mg_angl = 0.
    rtr_in_dm = 0.
    cr_thkns = 0.

    def calculate(self):
        """Doing the required calculation"""
        self.cr_thkns = (3.141592 * self.dr * self.bg) / (2 * self.nm * self.kst * self.bry)
        self.rtr_in_dm = 2 * ((self.dr / 2) - self.slv_thkn - self.mg_tkhn - self.cr_thkns)
        self.mg_angl = self.mg_cvrg * (360 / self.nm)

    def set_req_prmtr(self, args):
        """This method sets the required parameters for the current object of this class"""

        self.bg = args[0]
        self.kst = args[1]
        self.bry = args[2]
        self.nm = args[3]
        self.dr = args[4]
        self.mg_tkhn = args[5]
        self.mg_cvrg = args[6]

