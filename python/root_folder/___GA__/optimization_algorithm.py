"""This is the module containing different classes for the implementation of genetic algorithm
, this file will contain classes for fitness calculation, parent selection, crossover, mutation etc. All
 the class will be in the same file for ease"""

import math
import pandas
import random
from root_folder.program_data.fixed_program_data import fixed_data


class Fitness:
    """Data variables should be kept here for manipulation , this class is responsible for fitness
    evaluation of the chromosome of particular generation"""

    num_poles = None
    num_slots = None
    fill_fct = None
    stack_len = None
    rated_current = None
    motor_aspect_rto = None  #
    air_gap_len = None
    rotor_outer_dia = None
    rotor_inner_dia = None
    magnet_thick = None
    magnet_angle = None
    rotor_core_thick = None
    sleeve_thick = None
    magnet_tip_radius = None  #
    back_iron_depth = None
    shank_len = None
    tooth_tang_depth = None
    tooth_width = None
    tang_angle = None
    top_shaft_radius = None
    tooth_gap_angle = None
    num_skew_slots = None
    slot_area = None
    inner_diameter = None
    outer_diameter = None  #
    coil_span = None
    num_turns = None
    conductor_area = None
    rated_current_density = None

    def parse(self, args):
        """This function parses the tuple and assigns the values to the above variables"""
        self.num_poles = args[7]
        self.num_slots = args[8]
        self.fill_fct = args[9]
        self.stack_len = args[10]
        self.rated_current = args[11]
        self.motor_aspect_rto = args[12]
        self.air_gap_len = args[13]
        # -----------------------------------------------
        self.rotor_outer_dia = args[15]
        self.rotor_inner_dia = args[16]
        self.magnet_thick = args[17]
        self.magnet_angle = args[18]
        self.rotor_core_thick = args[19]
        self.sleeve_thick = args[20]
        self.magnet_tip_radius = args[21]
        # -----------------------------------------------
        self.back_iron_depth = args[23]
        self.shank_len = args[24]
        self.tooth_tang_depth = args[25]
        self.tooth_width = args[26]
        self.tang_angle = args[27]
        self.top_shaft_radius = args[28]
        self.tooth_gap_angle = args[29]
        self.num_skew_slots = args[30]
        self.slot_area = args[31]
        self.inner_diameter = args[32]
        self.outer_diameter = args[33]
        # ----------------------------------------------
        self.coil_span = args[35]
        self.num_turns = args[36]
        self.conductor_area = args[37]
        self.rated_current_density = args[38]

    def get_fitness_val(self):
        """Function to evaluate fitness of each solution based on the
        above parameters and  the generalised constraints"""
        wp = self.num_poles
        ws = self.num_slots
        # ---------calculation for poles and slots together-----------
        w1 = (0.08 * 1000 * (1 - math.exp(-(wp + ws) / 600000))
              + 0.08 * 1000 * (1 - math.exp(-self.outer_diameter / 100000)))
        # 600000 is the reference constant
        w2 = 0
        w5 = 0
        # ----air gap-------------------------------------------------
        if self.air_gap_len != 0:
            w2 = 0.25 * 1000 * (1 - math.exp(-0.1 / self.air_gap_len))  # 0.1 is the reference constant
        # check divide by zero error

        # -------fill factor------------------------------------------
        w3 = 0.25 * 1000 * (1 - math.exp(-self.fill_fct))
        # ---------rotor core thickness-------------------------------
        w4 = 0.15 * 1000 * (1 - math.exp(-self.rotor_core_thick / 1000))
        # ------sleeve thickness----------------
        if self.sleeve_thick != 0:
            w5 = 0.10 * 1000 * (1 - math.exp(-0.1 / self.sleeve_thick))  # check divide by zero error
        # --------magnet tip radius------------
        w6 = 0.08 * 1000 * (1 - math.exp(-self.magnet_tip_radius / 100))
        # ----------back iron depth------------
        w7 = 0.15 * 1000 * (1 - math.exp(-self.back_iron_depth / 1000))
        # ---------shank length--------------
        w8 = 0.20 * 1000 * (1 - math.exp(-self.shank_len / 1000))
        # ----------tooth tang depth------------
        w9 = 0.10 * 1000 * (1 - math.exp(-self.tooth_tang_depth / 400))
        # --------tooth width---------------
        w10 = 0.20 * 1000 * (1 - math.exp(-self.tooth_width / 700))
        # ------tang angle-----------------
        w11 = 0.25 * 1000 * (1 - math.exp(-self.tang_angle / 200))
        # ----------top shaft radius-------
        w12 = 0.10 * 1000 * (1 - math.exp(-self.top_shaft_radius / 30))
        # ----------tooth gap angle------------
        w13 = 0.10 * 1000 * (1 - math.exp(-self.tooth_gap_angle / 80))
        # ---------skew slots----------
        if self.num_skew_slots > 0:
            w14 = 0.29 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))
        else:
            w14 = 0
        # ------coil span---------------
        if self.coil_span == int(self.num_slots / self.num_poles) and int(self.num_slots / self.num_poles) >= 1:
            w15 = 0.22 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))
        elif self.coil_span == int(self.num_slots / self.num_poles) - 1 and int(self.num_slots / self.num_poles) >= 1:
            w15 = 0.35 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))
        elif self.coil_span == 0:
            w15 = -0.70 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))
        else:
            w15 = 0
        # -----------number of turns----------
        w16 = 0.40 * 1000 * (1 - math.exp(-self.num_turns / 1000))
        # ----------stack length-------------
        w17 = 0.85 * 1000 * (1 - math.exp(-self.stack_len / 12000))

        wi = w1 + w2 + w3 + w4 + w5 + w6 + w7 + w8 + w9 + w10 + w11 + w12 + w13 + w14 + w15 + w16 + w17

        """The constraint evaluation section starts here"""

        temp = [self.num_poles, self.num_slots, self.fill_fct, self.stack_len, self.rated_current,
                self.motor_aspect_rto, self.air_gap_len, self.rotor_outer_dia, self.rotor_inner_dia,
                self.magnet_thick, self.magnet_angle, self.rotor_core_thick, self.sleeve_thick,
                self.magnet_tip_radius, self.back_iron_depth, self.shank_len, self.tooth_tang_depth,
                self.tooth_width, self.tang_angle, self.top_shaft_radius, self.tooth_gap_angle, self.num_skew_slots,
                self.slot_area, self.inner_diameter, self.outer_diameter, self.coil_span, self.num_turns,
                self.conductor_area, self.rated_current_density]
        penalty = 0
        for i in temp:
            if i < 0:
                penalty += 60000 * (1 - math.exp(-self.outer_diameter / 10000))  # penalty for negative values
        """Below for each constraint violation a weighted penalty is assigned """
        wp1 = 0
        if self.num_poles != 0:
            q = (self.num_slots / self.num_poles) / 3  # 3 is the number of phase  # DBZ error
            if q <= 1.5:
                wp1 = (1.5 - q) * 0.40 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))
        wp2 = 0
        if self.rated_current_density > 3.5:
            wp2 = (self.rated_current_density - 3.5) * 0.60 * 8000 * (1 - math.exp(-self.outer_diameter / 10000))
        wp3 = 0
        if self.air_gap_len < math.fabs(0.01 * self.rotor_outer_dia):
            wp3 = 0.15 * 1000 * (1 - math.exp(-self.outer_diameter / 1000))
        wp4 = 0
        if self.fill_fct > 70:
            wp4 = (self.fill_fct - 70) * 0.40 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))

        wp5 = 0
        if self.num_poles != 0:
            wry_max = math.fabs((0.5 * 3.141592 * self.rotor_outer_dia * 1.001) / (2 * self.num_poles * 1))  # DBZ error
            # int he above formula | 1.001 is the air gap flux density and 1 is stacking factor

            if self.rotor_core_thick > wry_max:  # false comparison possible
                wp5 = (self.rotor_core_thick - wry_max) * 0.20 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))

        wp6 = 0
        const = self.magnet_tip_radius - math.fabs(0.30 * self.magnet_thick)  # false comparison possible
        if const > 0:
            wp6 = const * 0.05 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))

        wp7 = 0
        if self.num_poles != 0:
            wsy_max = math.fabs((0.5 * 3.141592 * self.rotor_outer_dia * 1.001) / (2 * self.num_poles * 1))  # DBZ error
            if self.back_iron_depth > wsy_max:  # false comparison possible
                wp7 = (self.back_iron_depth - wsy_max) * 0.20 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))

        wp8 = 0
        if self.outer_diameter != 0:
            rsr = (self.rotor_outer_dia / self.outer_diameter)  # take care of DBZ error during build
            if rsr < 0.50:
                wp8 = (0.50 - rsr) * 0.45 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))

        wp9 = 0
        if self.num_poles != 0:
            if 3 > (self.num_slots / self.num_poles) > 1:  # DBZ error
                wp9 = 0.60 * 2000 * (1 - math.exp(-self.outer_diameter / 10000))

        # ---------------------------------
        wp10 = 0
        wp11 = 0
        if self.tang_angle > 70:
            wp10 = self.tang_angle * 0.10 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))
        elif self.tang_angle < 30:  # taking care of divide by zero error
            if self.tang_angle == 0:
                wp11 = 0.10 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))
            elif self.tang_angle < 0:
                wp11 = math.fabs((1 / self.tang_angle) * 0.10 * 1000 * (1 - math.exp(-self.outer_diameter / 10000)))
            else:
                wp11 = (1 / self.tang_angle) * 0.10 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))
        wp12 = 0
        sk = int(self.num_slots / 20)
        if self.num_skew_slots > sk:
            wp12 = (self.num_skew_slots - sk) * 0.15 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))
        wp13 = 0
        wp14 = 0
        if self.num_poles != 0:
            if self.coil_span > math.fabs(int(self.num_slots / self.num_poles)):  # DBZ error
                wp13 = math.fabs((self.coil_span - math.fabs(int(self.num_slots / self.num_poles)))
                                 * 0.50 * 1000 * (1 - math.exp(-self.outer_diameter / 10000)))

            elif self.coil_span < (math.fabs(int(self.num_slots / self.num_poles)) - 1):  # DBZ error
                wp14 = math.fabs((math.fabs(int(self.num_slots / self.num_poles)) - 1 - self.coil_span)
                                 * 0.50 * 1000 * (1 - math.exp(-self.outer_diameter / 10000)))
        wp15 = 0
        if self.num_slots != 0:
            if self.tooth_gap_angle > math.fabs(0.20 * (360 / self.num_slots)):  # DBZ error
                wp15 = (self.tooth_gap_angle - math.fabs(0.2 * (360 / self.num_slots))) \
                       * 0.08 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))
        wp16 = 0
        if self.num_slots != 0:
            tth_max = math.fabs((0.65 * 3.141592 * 2 * (self.outer_diameter - self.back_iron_depth)) / self.num_slots)
            if self.tooth_width > tth_max:
                wp16 = (self.tooth_width - tth_max) * 0.11 * 1000 * (1 - math.exp(-self.outer_diameter / 10000))
        wp17 = 0
        if self.motor_aspect_rto > 3.5:
            wp17 = (self.motor_aspect_rto - 3.5) * 0.70 * 20000 * (1 - math.exp(-self.outer_diameter / 10000))
        elif self.motor_aspect_rto < 1.5:
            wp17 = (1.5 - self.motor_aspect_rto) * 0.75 * 50000 * (1 - math.exp(-self.outer_diameter / 10000))

        wpf = (wp1 + wp2 + wp3 + wp4 + wp5 + wp6 + wp7 + wp8 + wp9 + wp10 + wp11 + wp12 + wp13 + wp14 + wp15 + wp16 +
               wp17)

        """At last we are adding up all the values of : fitness, penalty, weighted penalty"""
        fit_val_ = wi - penalty - wpf

        return fit_val_


class ParentSelection:
    """Below defined is another class necessary for implementation of optimization algorithm,
    this class is responsible for selecting parent from the current generation"""

    def get_elites(self, read):

        """Creating list of indexes and fitness values from the current population"""
        fit_val = []
        fit_ind = []
        for index, row in read.iterrows():
            if index == 0 or index == 1:
                continue

            fit_tup = list(row)
            fit_ind.append(fit_tup[0])
            fit_val.append(fit_tup[39])

        """----------------------------------------------"""
        """pairing both the list in a dictionary"""

        dict_temp = dict.fromkeys(fit_ind)

        cnt = 0
        for key in dict_temp:
            dict_temp[key] = fit_val[cnt]
            cnt += 1

        fit_val.sort()
        elites = fit_val[920:]  # list of fitness of elite members
        del cnt
        """--------------------------------------"""
        """Getting the indexes of the elite members in the current population"""

        elite_ind = []

        for key in dict_temp:
            for i in range(0, 80):
                if dict_temp[key] == elites[i]:
                    elite_ind.append(key)

                else:
                    continue

        """-------------------------------------------------------------------"""
        """Getting the content of the elite members as tuple"""
        elite_mem = []
        for ind, rw in read.iterrows():
            if ind == 0 or ind == 1:
                continue
            for i in range(0, 80):
                if ind - 1 == elite_ind[i]:
                    tup = list(rw)
                    elite_mem.append(tup)
                else:
                    continue
        """------------------------------------------------------"""

        del read

        return elite_mem

    def select_parent(self, read):
        """code for select_parent method"""

        parent = []
        for m in range(0, 500):
            participants = []

            for i in range(0, 15):  # In single tournament 13 participants are there
                k = random.randint(3, 1000)
                participants.append(list(read.iloc[k + 1]))

            pa = participants[0]
            best = pa[39]
            best_ind = pa[0]

            for par in participants:

                if best < par[39]:
                    best = par[39]
                    best_ind = par[0]
                else:
                    continue

            parent.append(list(read.iloc[best_ind + 1]))
            del participants

        return parent


class NewGeneration:
    """This class is responsible for handling the mating process of the selected parents
    , it extracts the DNA from all the parents and does their mating. After that it builds the offspring
     chromosome and selects the best population among all"""

    def cross_over(self, parents):
        # extracting DNA from parents
        DNA = []
        for pr in parents:
            dna_lst = [pr[7], pr[8], pr[9], pr[10], pr[13], pr[19], pr[20], pr[21], pr[23],
                       pr[24], pr[25], pr[26], pr[27], pr[28], pr[29], pr[30], pr[35], pr[36]]

            DNA.append(dna_lst)

        # applying crossover on two random parent DNAs
        offspring_pop = []
        for x in range(0, 280):
            """now we have 920 DNAs we will select two at random"""
            ia = random.randint(0, 499)  # index of the selected DNA in the list
            ib = random.randint(0, 499)

            dna1 = list(DNA[ia])
            dna2 = list(DNA[ib])

            """now we are implementing one point simulated binary crossover , so we will select
            a random cross over point within the DNA size"""

            c_p = random.randint(0, 17)
            """now the genes from the index (c_p - 17) are applied to the crossover function as input
            and new values for those genes are created.
            Below are the tuning parameters for the crossover function, ui lies in (0.0, 1.0)"""
            ui = random.random()  # first parameter for probability function
            """The below parameter eta_c is responsible for the distance of offspring from the parent
            , the higher the value , more close offspring will be produced i.e. the value of the offspring
            gene will be more close to that of the parent gene."""
            eta_c = 0.8  # distribution index
            """Now the probability distribution function will be created, based on the value of 'ui' and 'eta_c'"""

            if ui <= 0.5:
                bqi = math.pow((2 * ui), (1 / (eta_c + 1)))
            else:
                bqi = math.pow((1 / (2 * (1 - ui))), (1 / (eta_c + 1)))

            """Now the segments of the offspring DNA will be calculated based on the above probability distribution 
            function, there will be two offspring segments. both the segments will contain the genes from the index
            (c_p - 17), now the new offspring DNA will consist two segments:-
             Parent DNA segment from index (0 - (c_p - 1)) + full offspring DNA segment"""
            # now below the crossover process is going on
            off_segment1 = []
            off_segment2 = []
            pt = c_p

            while pt <= 17:
                A = dna1[pt]
                B = dna2[pt]
                x = 0.5 * (((1 + bqi) * A) + ((1 - bqi) * B))
                y = 0.5 * (((1 - bqi) * A) + ((1 + bqi) * B))
                off_segment1.append(x)
                off_segment2.append(y)
                pt += 1
            """Now we have the two offspring segments in the above two list , we need to from the complete DNA by 
            attaching these to the unchanged parent DNA segment i.e. from the index 0 to c_p - 1"""

            offspring_dna1 = dna1[0:c_p] + off_segment1
            offspring_dna2 = dna2[0:c_p] + off_segment2

            offspring_pop.append(offspring_dna1)
            offspring_pop.append(offspring_dna2)

        return offspring_pop

    """Now here is the code for build method , this method is responsible for 
    creating full fledged chromosome from the offspring DNAs which will be used for further
     generations after evaluating their fitness"""

    def build_chromosome(self, off_dna_mat, parent):
        new_pop = []
        index = 1001
        for material in off_dna_mat:
            """These are the variables in the DNA list that participate in crossover """
            num_pole = material[0]
            num_slots = material[1]
            fill_f = material[2]
            stack_len = material[3]
            air_gp_len = material[4]
            rotor_cr_thk = material[5]
            sleeve_thk = material[6]
            mg_tpr = material[7]
            bck_ir_dpth = material[8]
            shnk_len = material[9]
            ttd = material[10]
            tth_wdth = material[11]
            tng_ang = material[12]
            tp_shft_rad = material[13]
            tth_gp_angl = material[14]
            skw_slt = material[15]
            cl_spn = int(material[16])
            num_turn = int(material[17])

            """Now we will calculate the rest of the variables of the chromosome using the above
            variables or genes, these variables are mentioned below """

            symbol = '|-'
            dc_volt = parent[2]
            rtd_spd = parent[3]
            rtd_trq = parent[4]
            out_dmr = parent[5]
            rtd_cur = parent[11]

            fitness_val = None

            """Now here we provide some strict guidance for few parameters to avoid
            the search from advancing in the completely undesired direction
            ,these are the naturally (practically) undeniable cases. It means these constraints must be 
            satisfied at any cost."""

            # for number of poles
            if int(num_pole) != num_pole:
                num_pole = int(num_pole)
            if (num_pole % 2) != 0:
                num_pole += 1
            if num_pole == 0:
                num_pole = 2
            if (num_pole % 6) == 0:
                num_pole += 2

            # for number of slots
            if int(num_slots) != num_slots:
                num_slots = int(num_slots)
            if (num_slots % 3) != 0:
                num_slots = num_slots + (3 - (num_slots % 3))
            if num_slots == 0:
                num_slots = 3

            # for coil span
            if num_pole > num_slots:
                if (num_slots % 2) == 0:
                    num_pole = num_slots
                else:
                    num_pole = num_slots - 1
            if cl_spn > int(num_slots / num_pole) or cl_spn == 0:
                cl_spn = int(num_slots / num_pole)

            # for sleeve thickness
            if rtd_spd > 5000 and sleeve_thk == 0:  # this ensures the presence of sleeve in high rpm
                sleeve_thk = (2 * random.random()) + 0.1

            # for tooth tang angle
            if tng_ang == 30:
                tng_ang = random.randint(31, 55)

            # for number of turns initially
            if num_turn == 0:
                num_turn = 1

            """The calculation process starts below"""
            mtr_as_rto = stack_len / out_dmr
            mag_thk = fixed_data.FixedParameters.mag_air_gp_rto * air_gp_len
            mag_ang = fixed_data.FixedParameters.mag_cvrg * (360 / num_pole)
            con = (out_dmr / 2) - bck_ir_dpth - shnk_len - ttd
            a = (1 - ((num_slots / (2 * 3.141592)) * tth_gp_angl))
            tng_ang_ln = (((2 * 3.141592 * (con + ttd) * a) - (num_slots * tth_wdth)) /
                          ((2 * num_slots) / math.tan((3.141592 / 180) * tng_ang)))

            inr_dmr_st = 2 * ((out_dmr / 2) - bck_ir_dpth - shnk_len - tng_ang_ln - ttd)
            rotor_out_dmr = inr_dmr_st - (2 * air_gp_len)
            rotor_in_dmr = 2 * ((rotor_out_dmr / 2) - mag_thk - rotor_cr_thk - sleeve_thk)
            r1 = (out_dmr / 2) - bck_ir_dpth
            r2 = r1 - shnk_len - tng_ang_ln
            arc = ((3.141592 / 180) * ((360 / num_slots) - tth_gp_angl)) * ((inr_dmr_st / 2) + ttd)
            tth_ara = (shnk_len * tth_wdth) + ((arc + tth_wdth) * tng_ang_ln)
            slt_ara = ((3.141592 * (r1 ** 2 - r2 ** 2)) / num_slots) - tth_ara
            cnd_area = (fill_f * slt_ara) / (num_turn * fixed_data.FixedParameters.winding_lyr)
            rtd_cur_dn = rtd_cur / cnd_area

            # for magnet tip radius
            if mg_tpr == 0:
                mg_tpr = ((random.random()) / 5) * mag_thk

            # for top shaft radius
            if tp_shft_rad == 0.02:
                tp_shft_rad = (random.random()) / 2

            # for number of skew slots
            if skw_slt == 1:  # possibility of empty range for randrange
                if num_slots < 20:
                    skw_slt = 1
                else:
                    skw_slt = random.randint(0, int(num_slots / 20))
            else:
                skw_slt = int(skw_slt)

            # for number of turns on the basis of rated current density
            if 2 > rtd_cur_dn >= 1.5:
                num_turn *= 2
            if 1.0 > rtd_cur_dn >= 0.5:
                num_turn *= 3
            if 0.5 > rtd_cur_dn >= 0.3:
                num_turn *= 8
            if 0.3 > rtd_cur_dn > 0.1:
                num_turn *= 10

            """after changing the number of turns current density and conductor area will also change,
            hence their new values are updated below"""
            cnd_area = (fill_f * slt_ara) / (num_turn * fixed_data.FixedParameters.winding_lyr)
            rtd_cur_dn = rtd_cur / cnd_area

            """Now if the inner diameter of rotor is very small it would be difficult to build a strong shaft
            hence it should not go below a certain limi which is specified below"""
            if rotor_in_dmr < (0.2 * rotor_out_dmr):
                rotor_in_dmr = 0.2 * rotor_out_dmr

            """Now the whole new chromosome is ready to be inserted in the new population, 
            and lies within the feasible zone. All the genes will be inserted in a list at their respective places"""
            insert = [index, symbol, dc_volt, rtd_spd, rtd_trq, out_dmr, symbol, num_pole, num_slots, fill_f,
                      stack_len, rtd_cur, mtr_as_rto, air_gp_len, symbol, rotor_out_dmr, rotor_in_dmr, mag_thk,
                      mag_ang, rotor_cr_thk, sleeve_thk, mg_tpr, symbol, bck_ir_dpth, shnk_len, ttd, tth_wdth,
                      tng_ang, tp_shft_rad, tth_gp_angl, skw_slt, slt_ara, inr_dmr_st, out_dmr, symbol,
                      cl_spn, num_turn, cnd_area, rtd_cur_dn, fitness_val]

            """Now inserted in the new population"""
            new_pop.append(insert)
            index += 1

        return new_pop
