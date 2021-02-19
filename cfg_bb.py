import sys
from copy import deepcopy


f = open(sys.argv[1], "r")
Lines = f.readlines()

total_line_count = 0
basic_block_id = 0
leaders = {}
successors = {}
First_List = []

for line in Lines:
    First_List.append([deepcopy(line).split(' ')[0].replace('\n',''), total_line_count])
    total_line_count = total_line_count+1

total_line_count = total_line_count-1

# find blocks first
line_count = 0
for line in Lines:
    if line_count == 0:
        leaders[basic_block_id] = line_count
        basic_block_id = basic_block_id + 1
    elif line.split(' ')[0] == "if":
        if line_count < total_line_count:
            leaders[basic_block_id] = line_count+1
            basic_block_id = basic_block_id + 1
        for x in First_List:
           if str(x[0]) == line.split(' ')[1].replace('\n',''):
               if x[1] in leaders.values():
                   break
               else:
                   leaders[basic_block_id] = x[1]
                   basic_block_id = basic_block_id + 1
                   break
    elif line.split(' ')[0] == "goto":
        for x in First_List:
           if str(x[0]) == line.split(' ')[1].replace('\n',''):
               if x[1] in leaders.values():
                   break
               else:
                   leaders[basic_block_id] = x[1]
                   basic_block_id = basic_block_id + 1
                   break
    
    line_count = line_count + 1

temp_leaders = {}
for x in leaders.keys():
    temp_leaders[x] = min(i for i in leaders.values())
    if x > 0:
        temp_leaders[x] = min(i for i in leaders.values() if i > temp_leaders[x-1])
    successors[x] = []

leaders = deepcopy(temp_leaders)

# get last line of blocks
last_line_leaders = {}
for x in leaders.keys():
    last_line_leaders[x] = -1

last_line_leaders[list(leaders.keys())[-1]] = total_line_count

line_count = 0
basic_block_id = 0
for line in Lines:
    if line.split(' ')[0] == "if" or line.split(' ')[0] == "goto":
        last_line_leaders[basic_block_id] = line_count
    if line_count > 0 and line_count in leaders.values():
        basic_block_id = basic_block_id + 1
        if last_line_leaders[basic_block_id-1] == -1:
            if line_count + 1 in leaders.values():
                last_line_leaders[basic_block_id-1] = line_count
            else:
                last_line_leaders[basic_block_id-1] = line_count - 1

    line_count = line_count + 1

basic_block_id = basic_block_id + 1

# find any dead code
temp_list = []
for x,y in leaders.items():
    for b in range(y, last_line_leaders[x]+1):
        temp_list.append(b)

line_count = 0
first_line = False
for line in Lines:
    if len(line.strip()) > 0:
        if line_count not in temp_list:
            if first_line == False:
                leaders[basic_block_id] = line_count
                first_line = True
            else:
                if line_count + 1 in temp_list:
                    last_line_leaders[basic_block_id] = line_count
                    basic_block_id = basic_block_id + 1
                    first_line = False

    line_count = line_count + 1

temp_leaders = {}
for x in leaders.keys():
    temp_leaders[x] = min(i for i in leaders.values())
    if x > 0:
        temp_leaders[x] = min(i for i in leaders.values() if i > temp_leaders[x-1])
    successors[x] = []

leaders = deepcopy(temp_leaders)

# find successors next
line_count = 0
basic_block_id = 0
for line in Lines:
    if line.split(' ')[0] == "if":
        if line_count < total_line_count:
            successors[basic_block_id] = [basic_block_id + 1]
        for x in First_List:
           if str(x[0]) == line.split(' ')[1].replace('\n',''):
               for key, value in leaders.items():
                   if value == x[1]:
                       successor_value = max(i for i in leaders.values() if i <= line_count)
                       for key1, value1 in leaders.items():
                           if value1 == successor_value:
                               successors.setdefault(key1, []).append(key) 
                               break
                       break
               break
    elif line.split(' ')[0] == "goto":
        for x in First_List:
           if str(x[0]) == line.split(' ')[1].replace('\n',''):
               for key, value in leaders.items():
                   if value == x[1]:
                       successor_value = max(i for i in leaders.values() if i <= line_count)
                       for key1, value1 in leaders.items():
                           if value1 == successor_value:
                               successors.setdefault(key1, []).append(key) 
                               break
                       break
    if line_count > 0 and line_count in leaders.values():
        basic_block_id = basic_block_id + 1
        if not successors[basic_block_id-1]:
            if basic_block_id-1 != max(leaders, key=int):
                successors[basic_block_id-1] = [basic_block_id]
    
    line_count = line_count + 1

temp_successors = deepcopy(successors)
for i,j in temp_successors.items():
    temp_values = []
    for x in j:
        if x not in temp_values:
            temp_values.append(x)
    temp_successors[i] = deepcopy(temp_values)

successors = deepcopy(temp_successors)

p = open("cfg.txt", "w")
for k,v in sorted(successors.items()):
    p.write(str(k) + ' => ')
    for x in v:
        p.write(str(x) + ' ')
    p.write("\n")