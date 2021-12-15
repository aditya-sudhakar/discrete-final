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
mypath = './auto-placement_project/auto-placement_project.kicad_pcb'
text_file = open(mypath, "r")
data = text_file.read()
text_file.close()
splits = data.split('(footprint')

##### IMPORTS #####
import math
from re import I
import sympy

##### FUNCTIONS #####

def consume_circuit(read_data):
    # Turn kicad pcb into python-usable format

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
    # Determine necessary grid size for optimzing placements

    max_grid_len = (math.ceil(math.sqrt(num_components))+1)**2
    # print(max_grid_len)
    # print(most_verticies_single)

    while_cond = (max_grid_len/2)**2
    while while_cond <= most_verticies_single/2:
        max_grid_len += 1
        while_cond = (max_grid_len/2)**2

    if max_grid_len%2 == 0:
        max_grid_len += 1

    print(f"The layout shall contain {max_grid_len} by {max_grid_len} slots.")

    return max_grid_len
    
def generate_grid(grid_len):

    grid = {}

    for i in range(grid_len):
        x_coord = 10*i
        grid[x_coord] = {}
        for j in range(grid_len):
            y_coord = 10*j
            if i%2 == 0:
                y_coord +=5
            grid[x_coord][y_coord] = False

    # print(grid)

    return grid

def calculate_min_thickness(vertices, edges):
    # calculate minimum layers number (derived from thickness)
    
    min_thickness = math.ceil(edges/(3*vertices-6))

    print(f"The minimum possible thickness for this graph is {min_thickness}.")
    print(f"A solution exists such that a complete PCB layout can achieved in {min_thickness} layers. ")
    
    return min_thickness

def squish(circuit_dict, general):
    # Place all components in a corner of the layout to keep things tidy


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
       
        # print(f"Component {component} moved to {new_loc}.")

        circuit_dict[component]['data'] = new_data
        f.write(circuit_dict[component]['data'])
    
    f.close()
    print('Board Squashed')
    print('PCB file updated.')

def update_location(circuit_dict, component, x_coord, y_coord):
    # Send placement info to kicad pcb file for updating
   
    f = open(mypath, 'w')
    f.truncate(0)
    f.write(general)

    circuit_dict[component]['location'][1] = x_coord
    circuit_dict[component]['location'][2] = y_coord
    circuit_dict[component]['location'][3] = 0

    circuit_dict[component]['location'][0] = f"(at {circuit_dict[component]['location'][1]} {circuit_dict[component]['location'][2]})"
    
    new_loc = circuit_dict[component]['location'][0]

    start_index = circuit_dict[component]['data'].find('(at')
    stop_index = circuit_dict[component]['data'].find(')', start_index) + 1 
    new_data = circuit_dict[component]['data'][:start_index] + new_loc + circuit_dict[component]['data'][stop_index:]
    
    print(f"Component {component} moved to {new_loc}.")

    circuit_dict[component]['data'] = new_data

    for component in circuit_dict:
        f.write(circuit_dict[component]['data'])

    print('PCB file updated.')

    return

def pick_next_component(circuit, placed_nets, placed_components, components_unused):
    
    # Currently chooses the next chronological component. Ultimately needs to
    # pick the next most optimal componant (based on what's placed)

    next_component = None

    temp_max_nets = 0
    for component in components_unused:
        if circuit[component]['total_pins'] > temp_max_nets:
            temp_max_nets = circuit[component]['total_pins']
            next_component = component

    if next_component == None:
        pass
    else:
        components_unused.remove(next_component)
        placed_components.append(next_component)
        for net in circuit[next_component]['netlist']:
            if net not in placed_nets:
                placed_nets.append(net)
        
    print(f'Now Placing {next_component}')

    return next_component, placed_nets, placed_components, components_unused

def place_next_component(grid, circuit_dict, next_component, placed_components, center_coord):
    # Place the desired component at the most optimal place

    x_coordinate = 0
    y_coordinate = 0


    if len(placed_components)  == 1:
        x_coordinate = center_coord
        y_coordinate = center_coord    

        grid[x_coordinate][y_coordinate] = next_component

        update_location(circuit_dict, next_component, x_coordinate, y_coordinate)


        for net in circuit_dict[next_component]['netlist']:
            if net not in netlist_dict:
                netlist_dict[net] = []

            if net in circuit_dict[next_component]['pins']['1']:
                netlist_dict[net].append((x_coordinate-0.9125, y_coordinate))
            else:
                netlist_dict[net].append((x_coordinate+0.9125, y_coordinate))

    else:
        min_x_coord, min_y_coord, cost = 0, 0, 9999999999
        temp_segments, temp_storage = [], []

        for x_c in list(grid.keys()):
            for y_c in list(grid[x_c].keys()):
                temp_cost, sum_cost = 999999999, 9999999999
                temp_segments, temp_points = [], []
                if grid[x_c][y_c] == False:
                    for net in circuit_dict[next_component]['netlist']:
                        # print(net)
                        if net not in netlist_dict:
                            netlist_dict[net] = []
                        if net in circuit_dict[next_component]['pins']['1']:
                            coord = (x_c-0.9125, y_c)
                        else:
                            coord = (x_c+0.9125, y_c)

                        temp_cost, shortest_segment = calculate_cost(net, coord, netlist_dict, segments, temp_segments, temp_points)
                        temp_segments.append(shortest_segment)
                        temp_points.append(coord)
                        temp_storage.append((net,temp_cost, shortest_segment, coord))

                        if sum_cost == 9999999999:
                            sum_cost = temp_cost
                        else:
                            sum_cost += temp_cost
                    # print(sum_cost)

                    if sum_cost < cost:
                        cost = sum_cost
                        temp_net1 = temp_storage[0][0]
                        segment1 = temp_storage[0][2]
                        coord_net1 = temp_storage[0][3]

                        temp_net2 = temp_storage[1][0]
                        segment2 = temp_storage[1][2]
                        coord_net2 = temp_storage[1][3]

                        min_x_coord = x_c
                        min_y_coord = y_c

        segments.append((segment1,temp_net1))
        segments.append((segment2,temp_net2))
        netlist_dict[temp_net1].append(coord_net1)
        netlist_dict[temp_net2].append(coord_net2)
        grid[min_x_coord][min_y_coord] = next_component
        update_location(circuit_dict, next_component, min_x_coord, min_y_coord)



    pass

def get_grid_center(grid,grid_len):
    #dangerous if indecies aren't lined up properly in the grid dict
    center_index = math.ceil(grid_len/2)
    center_coord = list(grid.keys())[center_index-1]

    return center_coord

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

def calculate_cost(net, coord, netlist_dict, segments, temp_segments, temp_points):

    cost = 0
    shortest_segment = None

    if len(netlist_dict) < 2:
        pass

    else:
        shortest_segment_length = 9999999
        for second_coord in netlist_dict[net]:
            if second_coord == coord:
                pass
            else:
                temp_segment =  sympy.Segment(sympy.Point(second_coord), sympy.Point(coord))
                if float(temp_segment.length) <= shortest_segment_length:
                    shortest_segment = temp_segment
                    shortest_segment_length = shortest_segment.length
        
        cost = shortest_segment_length
    
    if len(segments) > 1 and shortest_segment:
        for seg in segments:
            if seg[0] == shortest_segment:
                pass
            else:
                # print(seg[1], net)
                if seg[1] == net:
                    pass
                else:
                    if seg[0] == None:
                        pass
                    else:
                        if shortest_segment.intersection(seg[0]):
                            cost+=1000

    if len(temp_segments) > 0 and shortest_segment:
        for seg in temp_segments:
            if seg == shortest_segment:
                pass
            else:
                if shortest_segment.intersection(seg):
                    cost+=1000
    
    for point in temp_points:
        if point == None or shortest_segment == None:
            pass
        else:
            if sympy.Point(point).intersection(shortest_segment):
                cost += 1000
    
    for nets in netlist_dict:
        if nets != net:
            for point in netlist_dict[nets]:
                if shortest_segment:
                    if shortest_segment.intersection(sympy.Point(point)):
                        cost += 1000
    

    return cost, shortest_segment



def calculate_num_crossings():
    pass


if __name__ == "__main__":
    
    ### SETUP PHASE

    circuit_dict, num_nets, num_pins, num_components, most_pins_single, general = consume_circuit(data)
    
    num_edges, num_verticies = calculate_edges_verticies(num_pins, num_nets)
    min_thickness = calculate_min_thickness(num_verticies, num_edges)

    max_grid_len = calculate_grid_len(num_components, most_pins_single)

    netlist_dict = {}
    segments = []

    grid = generate_grid(max_grid_len)
    get_grid_center(grid, max_grid_len)
    squish(circuit_dict, general)

    placed_nets = []
    components_unused = list(circuit_dict.keys())
    components_unused.sort()
    placed_components = []
    center_coord = get_grid_center(grid,max_grid_len)


    ### LOOP/PLACE PHASE

    while len(components_unused) > 0:
        next_component, placed_nets, placed_components, components_unused = pick_next_component(circuit_dict, placed_nets, placed_components, components_unused)
        place_next_component(grid, circuit_dict, next_component, placed_components, center_coord)

