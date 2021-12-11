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

##### FILEPATH ######
mypath = './auto-placement_project/test.kicad_pcb'
text_file = open(mypath, "r")
data = text_file.read()
text_file.close()
splits = data.split('(footprint')

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
        pass


##### FUNCTIONS #####

def consume_circuit(read_data):
    circuit_dict = {}
    num_nets, num_pins, most_pins_single = 0, 0, 0
    splits = read_data.split('(footprint')
    general = ''

    for split in splits:
        if "general" in split:
            num_nets = split.count('(net') - 1
            general = split
        else:
            comp_name = find_refdes(split)
            circuit_dict[comp_name] = {"data":'(footprint' + split}
            # circuit_dict[comp_name] = {"data":0}

            netlist, total_pins, pins_dict = nets_on_component(split)
            circuit_dict[comp_name]['netlist'] = netlist
            circuit_dict[comp_name]['total_pins'] = total_pins
            circuit_dict[comp_name]['pins'] = pins_dict

            loc_str, x_coord, y_coord, theta = get_componet_location(split)
            circuit_dict[comp_name]['location'] = [loc_str, x_coord, y_coord, theta]

            num_pins += total_pins
            if total_pins > most_pins_single:
                most_pins_single = total_pins

    num_components = len(circuit_dict)
    # print(circuit_dict)

    print(f"There are {num_nets} unique nets and {num_pins} unique pins shared among {num_components} components in this circuit.")
    
    return circuit_dict, num_nets, num_pins, num_components, most_pins_single, general

def calculate_grid_len(num_components, most_verticies_single):

    max_grid_len = (math.ceil(math.sqrt(num_components))+1)**2

    while_cond = (max_grid_len-1)**2
    while while_cond < most_verticies_single/2:
        max_grid_len += 1
        while_cond = (max_grid_len-1)**2

    if max_grid_len%2 == 0:
        max_grid_len += 1

    print(f"The layout shall contain {max_grid_len} by {max_grid_len} slots.")

    return max_grid_len
    
def generate_grid(grid_len):
    #TODO IMPLEMENT
    pass

def calculate_min_thickness(vertices, edges):
    min_thickness = math.ceil(edges/(3*vertices-6))

    print(f"The minimum possible thickness for this graph is {min_thickness}.")
    print(f"A solution exists such that a complete PCB layout can achieved in {min_thickness-1} layers. ")
    
    return min_thickness

def squish(circuit_dict, general):

    f = open(mypath, 'w')
    f.truncate(0)
    f.write(general)
    
    for component in circuit_dict:

        f.write('\n')

        circuit_dict[component]['location'][1] = 0
        circuit_dict[component]['location'][2] = 0
        circuit_dict[component]['location'][3] = 0

        circuit_dict[component]['location'][0] = f"(at {circuit_dict[component]['location'][1]} {circuit_dict[component]['location'][2]})"
        
        new_loc = circuit_dict[component]['location'][0]

        start_index = circuit_dict[component]['data'].find('(at')
        stop_index = circuit_dict[component]['data'].find(')', start_index) + 1 
        new_data = circuit_dict[component]['data'][:start_index] + new_loc + circuit_dict[component]['data'][stop_index:]
       
        print(f"Component {component} moved to {new_loc}.")

        circuit_dict[component]['data'] = new_data
        f.write(circuit_dict[component]['data'])
    
    f.close()
    print('PCB file updated.')


def pick_next_component():
    #TODO IMPLEMENT
    pass

def optimize_me():
    #TODO IMPLEMENT
    pass


def find_refdes(component_string):
    start_index = component_string.find('(fp_text reference "') #19 characters long
    stop_index = component_string.find('"', start_index+20)
    ref_des = component_string[start_index+20:stop_index]
    return ref_des

def get_componet_location(component_string):
    x_coord, y_coord, theta = 0,0,0
    start_index = component_string.find('(at')
    stop_index = component_string.find(')', start_index) + 1 
    location_str = component_string[start_index+1:stop_index-1]

    loc_splits = location_str.split(" ")
    x_coord = float(loc_splits[1])
    y_coord = float(loc_splits[2])
    if len(loc_splits) == 4:
        theta = float(loc_splits[3])
    
    return location_str, x_coord, y_coord, theta
        
def nets_on_component(component_string):
    nets_list = []
    pin_dict = {}

    total_pins = 0
    temp_str = component_string
    while 'pad' in temp_str:
        temp_pad_loc = temp_str.find('pad')
        start_index = temp_str.find('"', temp_pad_loc)
        stop_index = temp_str.find('"', start_index+2)
        temp_pad = temp_str[start_index+1:stop_index]

        temp_pos_loc = temp_str.find('pad')
        start_index = temp_str.find('(at', temp_pos_loc)
        stop_index = temp_str.find(')', start_index) + 1 
        temp_pos = temp_str[start_index:stop_index]

        temp_net_loc = temp_str.find('net')
        start_index = temp_str.find('"', temp_net_loc)
        stop_index = temp_str.find('"', start_index+2)
        temp_net = temp_str[start_index+1:stop_index]

        if temp_net not in nets_list:
            nets_list.append(temp_net)

        pin_dict[temp_pad] = [temp_net, temp_pos]

        total_pins += 1
        temp_str = temp_str[stop_index:]
        
    return nets_list, total_pins, pin_dict

def calculate_edges_verticies(pins, nets):
    num_verticies = pins
    num_edges = pins-nets

    print(f"There shall be {num_edges} edges connecting {num_verticies} verticies in the target graph.")

    return num_edges, num_verticies


if __name__ == "__main__":
    circuit_dict, num_nets, num_pins, num_components, most_pins_single, general = consume_circuit(data)
    
    num_edges, num_verticies = calculate_edges_verticies(num_pins, num_nets)
    min_thickness = calculate_min_thickness(num_verticies, num_edges)

    max_grid_len = calculate_grid_len(num_components, most_pins_single)

    squish(circuit_dict, general)