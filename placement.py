######################################################################
#
# DISCRETE FINAL PROJECT 
#
# Date: December 2021
# 
# Contributors: Aditya Sudhakar, Lila Smith, Dasha Chadiuk
# 
# Description: 
#
#
######################################################################

##### IMPORTS #####
import math

##### CLASSES #####
class Resistor: 
    def __init__(self, name, p1_net, p2_net, x, y, theta, size):
        self.name = name        #Component Name, ex: R13, R21, etc.
        self.p1_net = p1_net    #Pad 1 net name, ex: GND
        self.p2_net = p2_net    #Pad 2 net name, ex: GND
        self.loc = [x,y,theta]  #Location of resistor [x-coord, y-coord, rotation]
        self.size = size        #size of resistor, ex: 0805, 0402, etc.
        self.p1_coord = []
        self.p2_coord = []

    def update_location(self,new_x, new_y, new_theta):
        self.loc = [new_x, new_y, new_theta]
        print(f"Location of {self.name} updated to {self.loc}")

    def calculate_pad_coords(self):
        

    




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