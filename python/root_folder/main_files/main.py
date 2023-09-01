"""This is the main file that handles the working of the individual modules
by using them in a proper sequence  . It is responsible for all the GUI operations
and acts as a bridge between the __GA__ modules and the geometry modules"""

from root_folder.program_data.variable_parameters_data.vector_parameters import Vectors
from root_folder.geometry_generator.general_sizing.sizing_parameters import Sizing
from root_folder.geometry_generator.rotor_geometry.rotor import RotorGeo
from root_folder.program_data.program_inputs.main_inputs import user_spec
from root_folder.geometry_generator.stator_geometry import stator
from tkinter import *
import pandas
from openpyxl import load_workbook
from root_folder.___GA__ import optimization_algorithm

"""GUI code segment below"""

mn_window = Tk()  # parent window

L1 = Label(mn_window, text='Supply voltage in VOLTS')
L1.grid(row=1, column=1)
a = StringVar()
E1 = Entry(mn_window, bg='white', bd='2', cursor='dot', textvariable=a)  # label with entry
E1.grid(row=1, column=2)
a.set("15.0")  # default value

L2 = Label(mn_window, text='Rated speed in RPM')
L2.grid(row=2, column=1)
b = StringVar()
E2 = Entry(mn_window, bg='white', bd='2', cursor='dot', textvariable=b)  # label with entry
E2.grid(row=2, column=2)
b.set("1000")  # default value

L3 = Label(mn_window, text='Rated torque in N-m')
L3.grid(row=3, column=1)
c = StringVar()
E3 = Entry(mn_window, bg='white', bd='2', cursor='dot', textvariable=c)  # label with entry
E3.grid(row=3, column=2)
c.set("1")  # default value

L4 = Label(mn_window, text='Outer Diameter of motor without casing in mm')
L4.grid(row=4, column=1)
d = StringVar()
E4 = Entry(mn_window, bg='white', bd='2', cursor='dot', textvariable=d)  # label with entry
E4.grid(row=4, column=2)
d.set("100")  # default value

"""Defining the button command method"""


def buttoncallback():
    v = a.get()
    sv = float(v)

    s = b.get()
    spd = float(s)

    t = c.get()
    trq = float(t)

    dr = d.get()
    dmr = float(dr)

    # todo : add an if else condition check for impractical input specification given by the user

    var = user_spec.Specification(sv, spd, trq, dmr)

    """Geometry calculator code below"""
    print('generating initial population')
    ct_lst = []
    us_lst = []
    sv_lst = []
    spd_lst = []
    trq_lst = []
    dmr_lst = []
    gs_lst = []
    n_p_lst = []
    s_l_lst = []
    f_f_lst = []
    stk_len_lst = []
    rtd_cur_lst = []
    m_asp_rto_lst = []
    a_gp_lst = []
    rp_lst = []
    rotor_od_lst = []
    rtr_in_dm_lst = []
    mg_thk_lst = []
    mg_ang_lst = []
    rtr_cr_thk_lst = []
    rtr_slv_thk_lst = []
    mg_tpr_lst = []
    sp_lst = []
    bck_ir_dpth_lst = []
    shnk_len_lst = []
    tng_dpth_lst = []
    tth_wdth_lst = []
    tth_tng_ang_lst = []
    tp_shft_rd_lst = []
    tth_gp_ang_lst = []
    skw_slt_lst = []
    slt_ara_lst = []
    inr_dmr_lst = []
    o_d_lst = []
    swp_lst = []
    cl_spn_lst = []
    n_t_lst = []
    cnd_ara_lst = []
    rtd_cur_den_lst = []
    fit_lst = []

    ct = 0
    for x in range(1, 1001):  # todo : add slider for generating variable size population in real time
        ct += 1
        vctr = Vectors()
        vc_tup = vctr.generate_random_set()

        # random set generated

        us_tup = var.get_req_prmtr_szng()
        szing = Sizing()
        szing.set_req_prmtr(vc_tup + us_tup)
        szing.calculate()

        # done sizing calculation

        st_tup = szing.get_req_prmtr_statr()
        statr = stator.StatorGeo()
        statr.set_req_prmtr(st_tup)
        statr.calculate()

        # done stator geometry calculation

        wndng = stator.StatorWinding()
        wnd_tup = szing.get_req_prmtr_wndng()
        l1 = list(wnd_tup)
        wnd_tup2 = statr.get_req_prmtr_wn()  # please take care at this block argument passing should be
        # in the right order
        l1.append(wnd_tup2)
        t1 = tuple(l1)
        wndng.set_req_prmtr(t1)
        wndng.calculate()

        # done winding calculation

        rt_tup = szing.get_req_prmtr_rotr()
        rtr = RotorGeo()
        rtr.set_req_prmtr(rt_tup)
        rtr.calculate()

        # done rotor calculation

        """All the calculation has been performed till this part of the code 
        now the results can be taken out for the chromosome generation. Here we are writing our data in excel sheet"""
        _chromosome_ = [ct, '|-', sv, spd, trq, dmr, '|-', szing.n_p, szing.s_l, szing.f_f, szing.stk_len,
                        wndng.rtd_cur, szing.m_as_rto, szing.a_gp, '|-', szing.rotor_od, rtr.rtr_in_dm,
                        szing.mg_tkh, rtr.mg_angl, rtr.cr_thkns, rtr.slv_thkn, rtr.mg_tp_r, '|-', statr.bck_ir_dpth,
                        statr.shnk_len, statr.tng_dpth, statr.tth_wdth, statr.th_tng_angl, statr.tp_shft_rd,
                        statr.tth_gp_angl, statr.skw_slots, statr.slt_ara, statr.inr_dmtr, statr.o_d, '|-',
                        wndng.cl_spn, wndng.n_t, wndng.cnd_ara, wndng.rtd_cur_den, 0]

        _fit_obj_ = optimization_algorithm.Fitness()
        _fit_obj_.parse(_chromosome_)
        ft_val_ = _fit_obj_.get_fitness_val()
        _chromosome_[39] = ft_val_
        print(_chromosome_)

        ct_lst.append(_chromosome_[0])
        # -----------------------------------------------
        us_lst.append(_chromosome_[1])
        sv_lst.append(_chromosome_[2])
        spd_lst.append(_chromosome_[3])
        trq_lst.append(_chromosome_[4])
        dmr_lst.append(_chromosome_[5])
        # --------------------------------------------------
        gs_lst.append(_chromosome_[6])
        n_p_lst.append(_chromosome_[7])
        s_l_lst.append(_chromosome_[8])
        f_f_lst.append(_chromosome_[9])
        stk_len_lst.append(_chromosome_[10])
        rtd_cur_lst.append(_chromosome_[11])
        m_asp_rto_lst.append(_chromosome_[12])
        a_gp_lst.append(_chromosome_[13])
        # ------------------------------------------------
        rp_lst.append(_chromosome_[14])
        rotor_od_lst.append(_chromosome_[15])
        rtr_in_dm_lst.append(_chromosome_[16])
        mg_thk_lst.append(_chromosome_[17])
        mg_ang_lst.append(_chromosome_[18])
        rtr_cr_thk_lst.append(_chromosome_[19])
        rtr_slv_thk_lst.append(_chromosome_[20])
        mg_tpr_lst.append(_chromosome_[21])
        # --------------------------------------------------
        sp_lst.append(_chromosome_[22])
        bck_ir_dpth_lst.append(_chromosome_[23])
        shnk_len_lst.append(_chromosome_[24])
        tng_dpth_lst.append(_chromosome_[25])
        tth_wdth_lst.append(_chromosome_[26])
        tth_tng_ang_lst.append(_chromosome_[27])
        tp_shft_rd_lst.append(_chromosome_[28])
        tth_gp_ang_lst.append(_chromosome_[29])
        skw_slt_lst.append(_chromosome_[30])
        slt_ara_lst.append(_chromosome_[31])
        inr_dmr_lst.append(_chromosome_[32])
        o_d_lst.append(_chromosome_[33])
        # ----------------------------------------------------
        swp_lst.append(_chromosome_[34])
        cl_spn_lst.append(_chromosome_[35])
        n_t_lst.append(_chromosome_[36])
        cnd_ara_lst.append(_chromosome_[37])
        rtd_cur_den_lst.append(_chromosome_[38])
        fit_lst.append(_chromosome_[39])

        """-------------------------------------------------------------------------------------------------------- """

        del vctr
        del szing
        del vc_tup
        del us_tup
        del st_tup  # all the results are deleted after use to free up memory.
        del wnd_tup
        del wnd_tup2
        del rt_tup
        del wndng
        del statr
        del rtr

    """Here we are assigning the list of individual genes to the dataframe and writing them in the database"""

    dat_fr = pandas.DataFrame({'chromosome': ct_lst, "****USER SPECIFICATION****": us_lst,
                               "DC supply voltage(volts)": sv_lst,
                               "Rated speed(rpm)": spd_lst, "Rated torque(N-m)": trq_lst,
                               "Outer diameter(mm)": dmr_lst,
                               "****GENERAL_SIZING****": gs_lst, "Number of poles": n_p_lst,
                               "Number of slots": s_l_lst,
                               "Fill factor": f_f_lst, "Stack length(mm)": stk_len_lst,
                               "Rated current(A)": rtd_cur_lst,
                               "Motor aspect ratio": m_asp_rto_lst, "air gap length": a_gp_lst,
                               "****ROTOR_PARAMETERS****": rp_lst,
                               "Rotor outer diameter(mm)": rotor_od_lst,
                               "Rotor inner diameter(mm)": rtr_in_dm_lst,
                               "Magnet thickness(mm)": mg_thk_lst, "Magnet angle(degree)": mg_ang_lst,
                               "Rotor core thickness(mm)": rtr_cr_thk_lst, "Sleeve thickness(mm)": rtr_slv_thk_lst,
                               "Magnet tip radius(mm)": mg_tpr_lst,
                               "****STATOR_PARAMETERS****": sp_lst,
                               "Back iron depth(mm)": bck_ir_dpth_lst,
                               "Shank length(mm)": shnk_len_lst, "Tooth tang depth(mm)": tng_dpth_lst,
                               "Tooth width(mm)": tth_wdth_lst,
                               "Tang angle(degree)": tth_tng_ang_lst,
                               "Top shaft radius(mm)": tp_shft_rd_lst,
                               "Tooth gap angle(degrees)": tth_gp_ang_lst,
                               " Number of skew slots": skw_slt_lst,
                               "Slot area(mm^2)": slt_ara_lst, "inner diameter(mm)": inr_dmr_lst,
                               "Outer_diameter(mm)": o_d_lst,
                               "****STATOR_WINDING_PARAMETERS****": swp_lst,
                               "Coil span": cl_spn_lst, "Number of turns": n_t_lst,
                               "Conductor area(mm^2)": cnd_ara_lst,
                               "Rated current density(A/mm^2)": rtd_cur_den_lst, "Fitness value": fit_lst})

    reader = pandas.read_excel('Process_Data_sheet.xlsx', sheet_name='Calculation_data_sheet')
    result = reader.append(dat_fr, ignore_index='True')
    result.to_excel('Process_Data_sheet.xlsx', sheet_name='Calculation_data_sheet', index=False)
    del reader


"""---------- Button function ends ---------------------------------------------------------------------------"""

"""Here we are using the pandas library to create an excel database where the data of the first generation 
will be stored , this database is created at the very beginning of the program before anything happens.
Later on the call of buttons the rest of processing starts."""

# creating a dataframe

df = pandas.DataFrame({'chromosome': 0, "****USER SPECIFICATION****": '|-', "DC supply voltage(volts)": '',
                       "Rated speed(rpm)": '', "Rated torque(N-m)": '', "Outer diameter(mm)": '',
                       "****GENERAL_SIZING****": '|-', "Number of poles": '',
                       "Number of slots": '',
                       "Fill factor": '', "Stack length(mm)": '', "Rated current(A)": '',
                       "Motor aspect ratio": '', "air gap length": '',
                       "****ROTOR_PARAMETERS****": '|-',
                       "Rotor outer diameter(mm)": '',
                       "Rotor inner diameter(mm)": '',
                       "Magnet thickness(mm)": '', "Magnet angle(degree)": '',
                       "Rotor core thickness(mm)": '', "Sleeve thickness(mm)": '',
                       "Magnet tip radius(mm)": '',
                       "****STATOR_PARAMETERS****": '|-', "Back iron depth(mm)": '',
                       "Shank length(mm)": '', "Tooth tang depth(mm)": '', "Tooth width(mm)": '',
                       "Tang angle(degree)": '', "Top shaft radius(mm)": '',
                       "Tooth gap angle(degrees)": '', " Number of skew slots": '',
                       "Slot area(mm^2)": '', "inner diameter(mm)": '', "Outer_diameter(mm)": '',
                       "****STATOR_WINDING_PARAMETERS****": '|-', "Coil span": '',
                       "Number of turns": '', "Conductor area(mm^2)": '',
                       "Rated current density(A/mm^2)": [''], "Fitness value": ''})

writer = pandas.ExcelWriter('Process_Data_sheet.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Calculation_data_sheet', index=False)
writer.save()
writer.close()
del writer

"""-----------------------------------------------------------------------------------------------------------"""

B1 = Button(mn_window, text='Generate population', command=buttoncallback)
B1.grid(row=5, column=2)  # Button for starting calculation

"""-----------------------------------------------------------------------------------------------------------"""
# todo: the below code should be included in the main window for another button callback
print('initial population generated')

"""code for application of genetic algorithm starts below"""


def GAcallback():
    for k in range(0, 10):
        read = pandas.read_excel('Process_Data_sheet.xlsx', sheet_name=k, header=None,
                                 index_col=None)

        """ Now passing the read object in the classes of optimization algorithm file to do the processing"""

        """ operation on current generation """

        opt = optimization_algorithm.ParentSelection()
        elites_members = opt.get_elites(read)  # fetching the elite members from the current population
        parents = opt.select_parent(read)  # fetching the parent members from the current population for mating process

        """ Now doing the processing for the next generation"""

        newgen = optimization_algorithm.NewGeneration()
        of_dna_lst = newgen.cross_over(parents)  # crossover process going on

        next_gen = newgen.build_chromosome(of_dna_lst, parents[0])  # building new offsprings in parents image

        """ Now evaluating the fitness of the new generation"""
        next_gen_fit = []
        s_fit_ = optimization_algorithm.Fitness()
        for sec in next_gen:
            inst = sec
            s_fit_.parse(sec)
            fit_vl_ = s_fit_.get_fitness_val()
            inst[39] = fit_vl_
            next_gen_fit.append(inst)
            del inst

        del next_gen

        """Now combining the whole population at one place 'transition'. This transition list is intermediate population
        between two generations and here the survival of fittest phenomena will occur """

        transition = elites_members + parents + next_gen_fit

        """Now getting the index with corresponding fitness of the new generation designate members"""
        i_list = []
        f_list = []
        h = 0
        for individual in transition:
            h += 1
            individual[0] = h
            i_list.append(h)
            f_list.append(individual[39])

        """Registering the new population"""
        new_gen_dict = dict.fromkeys(i_list)
        del i_list

        for i in new_gen_dict:
            new_gen_dict[i] = f_list[i - 1]

        """ selecting the top thousand members"""

        f_list.sort()  # arranging top 1000

        """Now we go for selecting individuals from the transition list , 
        here to maintain the diversity of the population, we are picking up the members from three segments 
        which have decreasing fitness in order"""

        n_f_list1 = f_list[600:]
        n_f_list2 = f_list[120:520]
        # always adjust these index according to the number of parents and off spring and elites taken
        n_f_list3 = f_list[20:80]

        new_list_fit = n_f_list1 + n_f_list2 + n_f_list3  # selected members

        new_ind_lst = []

        for chk in range(0, 1000):
            for key in new_gen_dict:
                if new_gen_dict[key] == new_list_fit[chk]:  # index of selected members
                    new_ind_lst.append(key)
                    break

        """---------------------------------------------------------------------------------------------------"""

        final_pop = []  # final population acquired

        for nw in new_ind_lst:
            final_pop.append(list(transition[nw - 1]))  # what is this problem ?

        c = 1
        for var in final_pop:  # arranging the index of the final population members
            var[0] = c
            c += 1

        del new_list_fit
        del new_ind_lst
        del n_f_list3
        del n_f_list2
        del n_f_list1
        del transition
        del new_gen_dict
        del opt
        del elites_members
        del parents
        del newgen
        del of_dna_lst

        """Now we have the final population of the next generation, we will write it into the excel sheet"""

        ct_lst = [0]
        us_lst = ['']
        sv_lst = ['']
        spd_lst = ['']
        trq_lst = ['']
        dmr_lst = ['']
        gs_lst = ['']
        n_p_lst = ['']
        s_l_lst = ['']
        f_f_lst = ['']
        stk_len_lst = ['']
        rtd_cur_lst = ['']
        m_asp_rto_lst = ['']
        a_gp_lst = ['']
        rp_lst = ['']
        rotor_od_lst = ['']
        rtr_in_dm_lst = ['']
        mg_thk_lst = ['']
        mg_ang_lst = ['']
        rtr_cr_thk_lst = ['']
        rtr_slv_thk_lst = ['']
        mg_tpr_lst = ['']
        sp_lst = ['']
        bck_ir_dpth_lst = ['']
        shnk_len_lst = ['']
        tng_dpth_lst = ['']
        tth_wdth_lst = ['']
        tth_tng_ang_lst = ['']
        tp_shft_rd_lst = ['']
        tth_gp_ang_lst = ['']
        skw_slt_lst = ['']
        slt_ara_lst = ['']
        inr_dmr_lst = ['']
        o_d_lst = ['']
        swp_lst = ['']
        cl_spn_lst = ['']
        n_t_lst = ['']
        cnd_ara_lst = ['']
        rtd_cur_den_lst = ['']
        fit_lst = ['']

        """Now getting the row variable from the final population"""

        for chrome in final_pop:
            _chromosome_ = chrome
            ct_lst.append(_chromosome_[0])
            # -----------------------------------------------
            us_lst.append(_chromosome_[1])
            sv_lst.append(_chromosome_[2])
            spd_lst.append(_chromosome_[3])
            trq_lst.append(_chromosome_[4])
            dmr_lst.append(_chromosome_[5])
            # --------------------------------------------------
            gs_lst.append(_chromosome_[6])
            n_p_lst.append(_chromosome_[7])
            s_l_lst.append(_chromosome_[8])
            f_f_lst.append(_chromosome_[9])
            stk_len_lst.append(_chromosome_[10])
            rtd_cur_lst.append(_chromosome_[11])
            m_asp_rto_lst.append(_chromosome_[12])
            a_gp_lst.append(_chromosome_[13])
            # ------------------------------------------------
            rp_lst.append(_chromosome_[14])
            rotor_od_lst.append(_chromosome_[15])
            rtr_in_dm_lst.append(_chromosome_[16])
            mg_thk_lst.append(_chromosome_[17])
            mg_ang_lst.append(_chromosome_[18])
            rtr_cr_thk_lst.append(_chromosome_[19])
            rtr_slv_thk_lst.append(_chromosome_[20])
            mg_tpr_lst.append(_chromosome_[21])
            # --------------------------------------------------
            sp_lst.append(_chromosome_[22])
            bck_ir_dpth_lst.append(_chromosome_[23])
            shnk_len_lst.append(_chromosome_[24])
            tng_dpth_lst.append(_chromosome_[25])
            tth_wdth_lst.append(_chromosome_[26])
            tth_tng_ang_lst.append(_chromosome_[27])
            tp_shft_rd_lst.append(_chromosome_[28])
            tth_gp_ang_lst.append(_chromosome_[29])
            skw_slt_lst.append(_chromosome_[30])
            slt_ara_lst.append(_chromosome_[31])
            inr_dmr_lst.append(_chromosome_[32])
            o_d_lst.append(_chromosome_[33])
            # ----------------------------------------------------
            swp_lst.append(_chromosome_[34])
            cl_spn_lst.append(_chromosome_[35])
            n_t_lst.append(_chromosome_[36])
            cnd_ara_lst.append(_chromosome_[37])
            rtd_cur_den_lst.append(_chromosome_[38])
            fit_lst.append(_chromosome_[39])

            """  dfrm = pandas.DataFrame({'chromosome': 0, "****USER SPECIFICATION****": '|-', 
            "DC supply voltage(volts)": '',
                                 "Rated speed(rpm)": '', "Rated torque(N-m)": '', "Outer diameter(mm)": '',
                                 "****GENERAL_SIZING****": '|-', "Number of poles": '',
                                 "Number of slots": '',
                                 "Fill factor": '', "Stack length(mm)": '', "Rated current(A)": '',
                                 "Motor aspect ratio": '', "air gap length": '',
                                 "****ROTOR_PARAMETERS****": '|-',
                                 "Rotor outer diameter(mm)": '',
                                 "Rotor inner diameter(mm)": '',
                                 "Magnet thickness(mm)": '', "Magnet angle(degree)": '',
                                 "Rotor core thickness(mm)": '', "Sleeve thickness(mm)": '',
                                 "Magnet tip radius(mm)": '',
                                 "****STATOR_PARAMETERS****": '|-', "Back iron depth(mm)": '',
                                 "Shank length(mm)": '', "Tooth tang depth(mm)": '', "Tooth width(mm)": '',
                                 "Tang angle(degree)": '', "Top shaft radius(mm)": '',
                                 "Tooth gap angle(degrees)": '', " Number of skew slots": '',
                                 "Slot area(mm^2)": '', "inner diameter(mm)": '', "Outer_diameter(mm)": '',
                                 "****STATOR_WINDING_PARAMETERS****": '|-', "Coil span": '',
                                 "Number of turns": '', "Conductor area(mm^2)": '',
                                 "Rated current density(A/mm^2)": [''], "Fitness value": ''})"""

        """First of all the column headers are written , after that the corresponding values will be written"""

        dfrm = pandas.DataFrame({'chromosome': ct_lst, "****USER SPECIFICATION****": us_lst,
                                 "DC supply voltage(volts)": sv_lst,
                                 "Rated speed(rpm)": spd_lst, "Rated torque(N-m)": trq_lst,
                                 "Outer diameter(mm)": dmr_lst,
                                 "****GENERAL_SIZING****": gs_lst, "Number of poles": n_p_lst,
                                 "Number of slots": s_l_lst,
                                 "Fill factor": f_f_lst, "Stack length(mm)": stk_len_lst,
                                 "Rated current(A)": rtd_cur_lst,
                                 "Motor aspect ratio": m_asp_rto_lst, "air gap length": a_gp_lst,
                                 "****ROTOR_PARAMETERS****": rp_lst,
                                 "Rotor outer diameter(mm)": rotor_od_lst,
                                 "Rotor inner diameter(mm)": rtr_in_dm_lst,
                                 "Magnet thickness(mm)": mg_thk_lst, "Magnet angle(degree)": mg_ang_lst,
                                 "Rotor core thickness(mm)": rtr_cr_thk_lst, "Sleeve thickness(mm)": rtr_slv_thk_lst,
                                 "Magnet tip radius(mm)": mg_tpr_lst,
                                 "****STATOR_PARAMETERS****": sp_lst,
                                 "Back iron depth(mm)": bck_ir_dpth_lst,
                                 "Shank length(mm)": shnk_len_lst, "Tooth tang depth(mm)": tng_dpth_lst,
                                 "Tooth width(mm)": tth_wdth_lst,
                                 "Tang angle(degree)": tth_tng_ang_lst,
                                 "Top shaft radius(mm)": tp_shft_rd_lst,
                                 "Tooth gap angle(degrees)": tth_gp_ang_lst,
                                 " Number of skew slots": skw_slt_lst,
                                 "Slot area(mm^2)": slt_ara_lst, "inner diameter(mm)": inr_dmr_lst,
                                 "Outer_diameter(mm)": o_d_lst,
                                 "****STATOR_WINDING_PARAMETERS****": swp_lst,
                                 "Coil span": cl_spn_lst, "Number of turns": n_t_lst,
                                 "Conductor area(mm^2)": cnd_ara_lst,
                                 "Rated current density(A/mm^2)": rtd_cur_den_lst, "Fitness value": fit_lst})

        book = load_workbook(r'Process_Data_sheet.xlsx')
        wrter = pandas.ExcelWriter('Process_Data_sheet.xlsx', engine='openpyxl')
        wrter.book = book
        dfrm.to_excel(wrter, sheet_name='Calculation_data_sheet', index=False)
        wrter.save()
        wrter.close()

        """reader = pandas.read_excel('Process_Data_sheet.xlsx', sheet_name=k+1)
        result = reader.append(dat_fr, ignore_index='True')
        result.to_excel('Process_Data_sheet.xlsx', sheet_name='Calculation_data_sheet', index=False)
        del reader"""


"""Button for applying GA to the geometry"""
B2 = Button(mn_window, text='Apply GA', command=GAcallback)
B2.grid(row=6, column=2)  # Button for starting calculation

mn_window.mainloop()
