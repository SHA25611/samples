import pandas
from root_folder.___GA__ import optimization_algorithm
from root_folder.program_data.fixed_program_data import fixed_data
import random
import math
import cmath

k = 0  # reading the kth sheet from the program workbook(Database)
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
n_f_list2 = f_list[120:520]  # always adjust these index according to the number of parents and off spring and elites
n_f_list3 = f_list[20:80]

new_list_fit = n_f_list1 + n_f_list2 + n_f_list3  # selected members

new_ind_lst = []

for chk in range(0, 1000):
    for key in new_gen_dict:
        if new_gen_dict[key] == new_list_fit[chk]:  # index of selected members
            new_ind_lst.append(key)
            break

"""------------------------------------------------------------------------------------------------------------"""

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
