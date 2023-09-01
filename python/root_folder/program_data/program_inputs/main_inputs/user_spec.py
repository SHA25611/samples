"""This file is the user specification file and it can be modified to take as many user inputs
as required in future"""


class Specification:
    """This class contains user specifications and methods to handle them"""
    sup_volt = 0  # volts
    rtd_spd = 0  # rpm
    rtd_trq = 0  # N-m(Newton-meter)
    out_dmtr = 0  # mm(millimeters)

    def __init__(self, sv, rspd, rtrq, odmtr):
        Specification.sup_volt = sv
        Specification.rtd_spd = rspd
        Specification.rtd_trq = rtrq
        Specification.out_dmtr = odmtr

    def get_req_prmtr_szng(self):
        """This function just returns the value for further calculation"""
        return self.sup_volt, self.rtd_spd, self.rtd_trq, self.out_dmtr

