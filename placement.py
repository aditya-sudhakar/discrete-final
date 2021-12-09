######################################################################
#
# DISCRETE FINAL PROJECT 
#
# Date: December 2021
# 
# Contributors: Aditya Sudhakar, Lila Smith, Dasha Chadiyuk
# 
# Description: 
#
#
######################################################################

##### IMPORTS #####
import math




##### FUNCTIONS #####

def consume_circuit():
    #TODO IMPLEMENT
    pass

def generate_netlist_dict():
    #TODO IMPLEMENT
    pass
    return netlist_dict, num_verticies, num_edges, num_components, most_verticies_single

def component_list_of_nets():
    #TODO IMPLEMENT
    pass

def calculate_grid_len(num_components, most_verticies_single):
    #TODO IMPLEMENT
    max_grid_len = (math.ceil(math.sqrt(num_components))+1)**2

    while_cond = (max_grid_len-1)**2
    while while_cond < most_verticies_single/2:
        max_grid_len += 1
        while_cond = (max_grid_len-1)**2

    if max_grid_len%2 == 0:
        max_grid_len += 1

    return max_grid_len
    
def generate_grid(grid_len):
    #TODO IMPLEMENT
    pass

def calculate_min_thickness(vertices, edges):
    min_thickness = math.ceil(edges/(3*vertices-6))
    return min_thickness

def squish():
    #TODO IMPLEMENT
    pass

def pick_next_component():
    #TODO IMPLEMENT
    pass

def optimize_me():
    #TODO IMPLEMENT
    pass