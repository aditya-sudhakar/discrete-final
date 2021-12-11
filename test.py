

mypath = './auto-placement_project/auto-placement_project.kicad_pcb'

text_file = open(mypath, "r")

data = text_file.read()

text_file.close()

print(type(data))


splits = data.split('(footprint')

testcomp = splits[1]
print(testcomp)

start_index = testcomp.find('(at')
print(start_index)
stop_index = testcomp.find(')', start_index) + 1 
print(stop_index)

print(testcomp[start_index:stop_index])


start_index = testcomp.find('(fp_text reference "') #19 characters long
print(start_index)
stop_index = testcomp.find('"', start_index+20)
print(stop_index)
ref_des = testcomp[start_index+20:stop_index]

print(ref_des)



# print(len(splits))
# print(type(splits))

# print(splits[1])

